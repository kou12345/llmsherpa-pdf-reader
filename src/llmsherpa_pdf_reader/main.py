import os
from llmsherpa.readers import LayoutPDFReader

# 定数
LLMSHERPA_API_URL = "http://localhost:5010/api/parseDocument?renderFormat=all"
PDF_PATH = "/Users/kou12345/Downloads/データ指向アプリケーションデザイン.pdf"
OUTPUT_DIR = "output"


def ensure_output_directory(directory):
    """出力ディレクトリが存在することを確認する"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_to_file(filename, content):
    """出力ディレクトリにコンテンツをファイルとして書き込む"""
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
        f.write(content)


def process_sections(sections):
    """セクションを処理し、異なる出力形式を返す"""
    text_output = ""
    html_output = ""
    context_text_output = ""
    for section in sections:
        text_output += section.to_text(include_children=True, recurse=True) + "\n"
        html_output += section.to_html(include_children=True, recurse=True) + "\n"
        context_text_output += section.to_context_text(include_section_info=True)
    return text_output, html_output, context_text_output


def process_tables(tables):
    """テーブルを処理し、テキスト出力を返す"""
    return "\n".join(table.to_text() for table in tables)


def main():
    # PDFリーダーを初期化し、ドキュメントを読み込む
    pdf_reader = LayoutPDFReader(LLMSHERPA_API_URL)
    doc = pdf_reader.read_pdf(PDF_PATH)

    # セクションとテーブルを抽出
    sections = doc.sections()
    tables = doc.tables()

    chunks = doc.chunks()
    all_chunk_text = ""
    for chunk in chunks:
        all_chunk_text += "Chunk:\n" + chunk.to_text() + "\n-----\n"

    write_to_file("all_chunk_text.txt", all_chunk_text)

    # セクションを処理
    text_output, html_output, context_text_output = process_sections(sections)

    # テーブルを処理
    table_output = process_tables(tables)

    # 出力ディレクトリが存在することを確認
    ensure_output_directory(OUTPUT_DIR)

    # 出力をファイルに書き込む
    write_to_file("text_output.txt", text_output)
    write_to_file("html_output.html", html_output)
    write_to_file("context_text_output.txt", context_text_output)
    write_to_file("table_output.txt", table_output)

    print(
        "処理が完了しました。出力ファイルは 'output' ディレクトリに生成されています。"
    )


if __name__ == "__main__":
    main()

"""
出力品質に関する注記：
- section.to_text(): かなり良い
- section.to_html(): かなり良い、非常に見やすい
- table.to_html(): 微妙、元のPDFの表の品質が良くない可能性がある
- table.to_text(): 良い
- section.to_text()でもテーブルを綺麗に出力できているようだ
- section.to_context_text(): 用途が不明、さらなる調査が必要
"""
