from easy_patents.get_info import app_progress
from easy_patents.errors import NoDocumentError, TooManyAccessError, ParameterError, UnknownError
import configparser
from mail_notify import email
import pandas as pd
from datetime import datetime, timedelta


def check_due_date(excel_path, sheet_name="Sheet1", from_addr="", to_addrs=[]):
    '''
    中間処理の対応状況を確認する
    最新の拒絶理由に対して、その後に意見書が提出されているかをチェックし、
    その状況をエクセルに記録する。
    新しい拒絶理由、日付の近い拒絶理由に対してはメール送信

    Parameters
    ----------
    excel_path: str
        更新対象のエクセルのパス
    sheet_name: str or int
        シート名またはシート番号
    '''
    # 指定されたエクセルを読み出す
    #df = pd.read_excel(excel_path, sheet_name=sheet_name)

    # インストールしたpandasのバージョンによっては、以下のようにencodingを指定する必要がある。
    df = pd.read_excel(excel_path,
            sheet_name=sheet_name, encoding="utf-8_sig")

    for index, row in df.iterrows():

        last_rejection_date = row['rejection_date']
        # データの初期化
        row['rejection_date'] = ''
        row['due_date'] = ''
        row['warning'] = ''
        row['opinion_submit_date'] = ''
        row['invention_title'] = ''
        subject = ""
        body = ""

        # 読み込んだエクセルから出願番号を取得
        app_number = row['app_number']

        # 特許経過情報の取得
        try:
            progress_info = app_progress(app_number, reget_date=7)
        except NoDocumentError:
            # 未公開情報などでドキュメントが取得できない場合にはスキップ
            continue
        except ParameterError as e:
            # パラメーターエラーの場合（出願番号の記載に誤りがあるような場合）には、
            # メッセージを出してスキップ
            print(e)
            continue
        except (TooManyAccessError, UnknownError) as e:
            # アクセス数超過、原因不明エラーの場合には
            # エラーメッセージを出力して終了
            print(e)
            break


        # 発明の名称を設定
        row['invention_title'] = progress_info['result']['data']['inventionTitle']

        # 拒絶理由通知書と意見書の書類データの抽出
        document_list = get_documents_info(progress_info)
        rejection_list = pickup_documents_info(document_list, "拒絶理由通知書")
        opinion_list = pickup_documents_info(document_list, "意見書")

        # 拒絶理由がない場合には、次のループへ
        if len(rejection_list) == 0:
            continue

        # legalDateで並び替え
        sort_key = lambda x : x['legalDate']
        rejection_list.sort(key=sort_key)
        opinion_list.sort(key=sort_key)

        # 最新の拒絶理由を取得
        latest_rejection = rejection_list[-1]
        
        # 拒絶理由通知の日付を格納
        rejection_date = datetime.strptime(latest_rejection['legalDate'], "%Y%m%d")
        row['rejection_date'] = rejection_date

        # 応答期限を取得(本例では、暫定的に60日期限,土日等の繰り越しなし)
        due_date = rejection_date + timedelta(days=60)
        row['due_date'] = due_date

        # 拒絶理由通知の日付以後の意見書提出がないことを示すフラグを設定
        not_submitted_flag = True

        if len(opinion_list) != 0:
            latest_opinion = opinion_list[-1]
            opinion_date = datetime.strptime(latest_opinion['legalDate'], "%Y%m%d")
            # 意見書の日付が拒絶理由通知の日付以後の場合に、
            # opinion_submit_dateに日付を記入
            # これ以外の場合には追記しない。
            if opinion_date >= rejection_date:
                row['opinion_submit_date'] = opinion_date
                not_submitted_flag = False

        # 応答期限までの日数が0日以上の場合には、あと〇日という警告を出力
        now = datetime.now()
        days_by_due_date = due_date - now
        if -1 < days_by_due_date.days and not_submitted_flag:
            row['warning'] = "あと%s日" % days_by_due_date.days

        # 応答期限までの日数が-1から-30日の場合には、期限切れという警告を出力
        if -30 <= days_by_due_date.days <= -1 and not_submitted_flag:
            row['warning'] = "期限切れ"

        # データフレームの対象行を取得した情報でアップデート
        df.loc[index] = row

        # メール設定読み込み
        config = configparser.ConfigParser()
        config.read('mail_config.ini')
        user = config['Email']['user']
        password = config['Email']['password']
        smtp_server = config['Email']['smtp_server']
        smtp_port = config['Email']['smtp_port']
        is_ssl = config['Email']['is_ssl']

        # 応答期限まで14日未満の場合、メール送信
        if  -1 < days_by_due_date.days < 14:
            subject = "拒絶理由応答期限まであと%s日" % days_by_due_date.days
            body = "出願番号: %s\n対応期限: %s" % (app_number, due_date)
        # 拒絶理由の日付が違う場合、すなわち、新たな拒絶理由を受けた場合、メール送信
        elif rejection_date != last_rejection_date:
            subject = "新たな拒絶理由通知を受けました"
            body = "出願番号: %s\n対応期限: %s" % (app_number, due_date)

        if subject:
            email(
                   fromaddr=from_addr,
                   toaddrs=to_addrs,
                   smtp_server=smtp_server,
                   smtp_port=smtp_port,
                   subject=subject,
                   body=body,
                   is_ssl=is_ssl,
                   user=user,
                   password=password,
            )

    # エクセルに反映
    #df.to_excel(excel_path,
    #        sheet_name=sheet_name, index=False)

    # インストールしたpandasのバージョンによっては、以下のようにencodingを指定する必要がある。
    df.to_excel(excel_path,
          sheet_name=sheet_name, index=False, encoding="utf-8_sig")


def get_documents_info(progress_info):
    '''
    bibliographyInformation以下のdocumentデータを一つのリストにまとめる関数

    Parameters
    ----------
    progress_info: json
        app_progressで取得されるjsonデータ

    Returns
    -------
    list
        書類情報データのリスト
    '''
    document_list = []
    for binfo in progress_info['result']['data']['bibliographyInformation']:
        document_list += binfo['documentList']
    return document_list


def pickup_documents_info(document_list, document_name):
    '''
    document_listからdocumentDescriptionがdocument_nameであるものを抽出する関数

    Parameters
    ----------
    document_list: list
        app_progressのbibliographyInformation以下のdocumentListを一つにまとめたリスト
        もしくは、app_progressのbibliographyInformation以下のいずれかのdocumentList
    document_name: str
        抽出対象の書類名

    Returns
    -------
    list
        抽出対象の書類データのリスト
    '''
    ret = []
    for document in document_list:
        if document['documentDescription'] == document_name:
            ret.append(document)
    return ret


if __name__ == "__main__":
    import sys
    excel_path = sys.argv[1]
    sheet_name = sys.argv[2]
    from_addr = sys.argv[3]
    to_addrs = sys.argv[4:]
    check_due_date(excel_path, sheet_name, from_addr, to_addrs)
