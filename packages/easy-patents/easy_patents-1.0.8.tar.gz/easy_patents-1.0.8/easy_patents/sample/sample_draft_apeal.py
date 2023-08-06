from easy_patents.get_info import app_progress
from datetime import datetime as dt
import mojimoji


def make_progress_message(app_number):
    progress_info = app_progress(app_number)
    target_docs = {
            "拒絶理由通知書",
            "拒絶査定",
            "補正の却下の決定",
            "手続補正書",
            "意見書",
            "出願審査請求書",
            "特許願"
    }

    biblio_info = progress_info['result']['data']['bibliographyInformation']
    doc_info_list = [doc_info for biblio in biblio_info 
            for doc_info in biblio["documentList"]]
    target_doc_info_list = [doc_info for doc_info in doc_info_list 
            if doc_info['documentDescription'] in target_docs]

    target_doc_info_list.sort(key=lambda x:x['legalDate'])
    ret = []
    message_length = 25
    for target_doc_info in target_doc_info_list:
        legal_date = dt.strptime(target_doc_info['legalDate'], "%Y%m%d")
        document_desc = target_doc_info['documentDescription']
        legal_date_str = legal_date.strftime('%Y年%m月%d日')
        legal_date_str = mojimoji.han_to_zen(legal_date_str)
        space_length = message_length - len(document_desc) - len(legal_date_str)
        message = document_desc + "　" * space_length + legal_date_str
        ret.append(message)
    return '\n'.join(ret)


if __name__ == "__main__":
    print(make_progress_message("2007-035937"))

