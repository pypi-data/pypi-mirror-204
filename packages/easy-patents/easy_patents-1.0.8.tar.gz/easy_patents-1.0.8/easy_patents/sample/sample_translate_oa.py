import os
import xml.etree.ElementTree as ET
from sample_translate import get_translation
from easy_patents.get_info import app_doc_cont_refusal_reason_decision
from easy_patents.get_info import app_progress


def translate_latest_refusal_reason(app_number, deepl_auth_key, target_lang="En"):
    # 特許庁APIを通じて、経過情報と拒絶理由通知書ファイルをダウンロード
    progress_info = app_progress(app_number)
    target_dir_path = app_doc_cont_refusal_reason_decision(app_number)

    # 経過情報から、拒絶理由通知書にかかる情報を抽出
    biblio_info = progress_info['result']['data']['bibliographyInformation']
    doc_info_list = [doc_info for biblio in biblio_info for doc_info in biblio["documentList"]]
    kyozetsu_doc_info_list = [doc_info for doc_info in doc_info_list if doc_info['documentDescription'] == "拒絶理由通知書"]

    # legalDateでソートして、最新の拒絶理由通知書のdocumentNumberを取得
    kyozetsu_doc_info_list.sort(key=lambda x:x['legalDate'])
    latest_kyozetsu = kyozetsu_doc_info_list[-1]
    latest_kyozetsu_docnumber = latest_kyozetsu["documentNumber"]

    # documentNumberをもとに、対象の拒絶理由通知書のxmlデータを読み込む。
    target_file_name = "%s-jpntce.xml" % latest_kyozetsu_docnumber
    target_file_path = os.path.join(target_dir_path, target_file_name)
    with open(target_file_path, "r", encoding="shift_jis") as f:
        target_xml_data = f.read()
    root = ET.fromstring(target_xml_data)

    # 読み込んだ拒絶理由通知書のデータから理由が書かれている部分を抽出
    ns = {'jp': 'http://www.jpo.go.jp'}
    sub1 = root.find('jp:notice-of-rejection-a131', ns)
    reason_part = sub1.find('jp:drafting-body', ns)
    reason_text = ''.join([text for part in reason_part for text in part.itertext()])
    reason_text = reason_text.replace("\n\n", " ")
    reason_text = reason_text.replace("\n", "")
    reason_text = reason_text.replace("　　", "\n")
    reason_text = reason_text.replace(" ", "\n")
    while "\n\n" in reason_text:
        reason_text = reason_text.replace("\n\n", "\n")

    # 抽出した部分をDeepLのAPIで翻訳し、翻訳前と翻訳後のテキストを返す
    translated_text = get_translation(reason_text, auth_key=deepl_auth_key, target_lang=target_lang)
    return reason_text, translated_text


if __name__ == "__main__":
    DEEPL_AUTH_KEY = "***"
    texts = translate_latest_refusal_reason("2007035937", deepl_auth_key=DEEPL_AUTH_KEY, target_lang="En")
    # 翻訳前のテキスト
    print(texts[0])
    # 翻訳後のテキスト
    print(texts[1])
