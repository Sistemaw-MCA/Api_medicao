from flask import Flask, request, send_file, jsonify
import os
import fitz  # PyMuPDF

app = Flask(__name__)

# Pasta temporária para salvar os arquivos (caminho absoluto)
UPLOAD_FOLDER = os.path.abspath('./uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Rota para conversão de PDF para HTML
@app.route('/convert', methods=['POST'])
def convert_pdf_to_html():
    try:
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400
        
        file = request.files['file']

        # Verifica se é um arquivo PDF
        if not file.filename.endswith('.pdf'):
            return jsonify({"error": "Por favor, envie um arquivo PDF."}), 400

        # Salva o arquivo PDF no diretório temporário
        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(pdf_path)

        # Define o caminho do arquivo de saída (HTML)
        output_html = os.path.join(UPLOAD_FOLDER, file.filename.replace('.pdf', '.html'))

        # Abrir o PDF usando PyMuPDF
        doc = fitz.open(pdf_path)

        # Iniciar o arquivo HTML
        html_content = "<html><body>"

        # Iterar sobre as páginas do PDF e extrair o conteúdo HTML
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            html_content += page.get_text("html")

        html_content += "</body></html>"

        # Salvar o conteúdo HTML em um arquivo
        with open(output_html, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)

        # Retorna o arquivo HTML convertido
        return send_file(output_html, as_attachment=True)

    except Exception as e:
        # Imprime o erro no console para depuração
        print(f"Erro durante a conversão: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
