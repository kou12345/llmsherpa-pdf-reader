from llmsherpa.readers import LayoutPDFReader

llmsherpa_api_url = "http://localhost:5010/api/parseDocument?renderFormat=all"
pdf_url = ""
pdf_reader = LayoutPDFReader(llmsherpa_api_url)
doc = pdf_reader.read_pdf(pdf_url)

sections = doc.sections()
tables = doc.tables()

text_output = ""
html_output = ""
context_text_output = ""
for section in sections:
    text_output += section.to_text(include_children=True, recurse=True) + "\n"
    html_output += section.to_html(include_children=True, recurse=True) + "\n"
    context_text_output += section.to_context_text(include_section_info=True)

with open("text_output.txt", "w") as f:
    f.write(text_output)

with open("html_output.html", "w") as f:
    f.write(html_output)

with open("context_text_output.txt", "w") as f:
    f.write(context_text_output)

table_output = ""
for table in tables:
    table_output += table.to_text() + "\n"

with open("table_output.txt", "w") as f:
    f.write(table_output)

print("Done!!!")

"""
section.to_text かなり良い
section.to_html かなり良い すごく見やすい

table.to_html 微妙 オリジナルPDFの表がよくない可能性もある
table.to_text 良い

section.to_textでもtableを綺麗に出力できているぽい

section.to_context_text 何に使うのか分からない
"""
