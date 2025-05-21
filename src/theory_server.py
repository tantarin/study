import markdown2
import webbrowser
import os
from src.bot.handlers import create_full_theory_markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import re
import html

def highlight_code(code, language):
    """Подсвечивает синтаксис кода с использованием Pygments"""
    try:
        lexer = get_lexer_by_name(language)
        formatter = HtmlFormatter(style='monokai')
        return highlight(code, lexer, formatter)
    except:
        return code

def convert_md_to_html(md_file_path):
    """Конвертирует Markdown файл в HTML с красивым оформлением и подсветкой синтаксиса"""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Добавляем CSS стили для красивого оформления и подсветки синтаксиса
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Теория для подготовки к собеседованиям</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                max-width: 900px;
                margin: 0 auto;
                padding: 2rem;
                background-color: #f5f5f5;
            }}
            h1, h2, h3, h4 {{
                color: #2c3e50;
                margin-top: 2rem;
            }}
            h1 {{
                border-bottom: 2px solid #3498db;
                padding-bottom: 0.5rem;
            }}
            pre {{
                background-color: #272822;
                padding: 1rem;
                border-radius: 4px;
                overflow-x: auto;
                margin: 1rem 0;
            }}
            code {{
                font-family: 'Fira Code', 'Consolas', monospace;
                color: #f8f8f2;
            }}
            .highlight {{
                margin: 1rem 0;
            }}
            .highlight pre {{
                margin: 0;
                background-color: #272822;
            }}
            .highlight .c {{
                color: #75715e;
            }}
            .highlight .err {{
                color: #960050;
                background-color: #1e0010;
            }}
            .highlight .k {{
                color: #66d9ef;
            }}
            .highlight .l {{
                color: #ae81ff;
            }}
            .highlight .n {{
                color: #f8f8f2;
            }}
            .highlight .o {{
                color: #f92672;
            }}
            .highlight .p {{
                color: #f8f8f2;
            }}
            .highlight .cm {{
                color: #75715e;
            }}
            .highlight .cp {{
                color: #75715e;
            }}
            .highlight .c1 {{
                color: #75715e;
            }}
            .highlight .cs {{
                color: #75715e;
            }}
            .highlight .ge {{
                font-style: italic;
            }}
            .highlight .gs {{
                font-weight: bold;
            }}
            .highlight .kc {{
                color: #66d9ef;
            }}
            .highlight .kd {{
                color: #66d9ef;
            }}
            .highlight .kn {{
                color: #f92672;
            }}
            .highlight .kp {{
                color: #66d9ef;
            }}
            .highlight .kr {{
                color: #66d9ef;
            }}
            .highlight .kt {{
                color: #66d9ef;
            }}
            .highlight .ld {{
                color: #e6db74;
            }}
            .highlight .m {{
                color: #ae81ff;
            }}
            .highlight .s {{
                color: #e6db74;
            }}
            .highlight .na {{
                color: #a6e22e;
            }}
            .highlight .nb {{
                color: #f8f8f2;
            }}
            .highlight .nc {{
                color: #a6e22e;
            }}
            .highlight .no {{
                color: #66d9ef;
            }}
            .highlight .nd {{
                color: #a6e22e;
            }}
            .highlight .ni {{
                color: #f8f8f2;
            }}
            .highlight .ne {{
                color: #a6e22e;
            }}
            .highlight .nf {{
                color: #a6e22e;
            }}
            .highlight .nl {{
                color: #f8f8f2;
            }}
            .highlight .nn {{
                color: #f8f8f2;
            }}
            .highlight .nx {{
                color: #a6e22e;
            }}
            .highlight .py {{
                color: #f8f8f2;
            }}
            .highlight .nt {{
                color: #f92672;
            }}
            .highlight .nv {{
                color: #f8f8f2;
            }}
            .highlight .ow {{
                color: #f92672;
            }}
            .highlight .w {{
                color: #f8f8f2;
            }}
            .highlight .mf {{
                color: #ae81ff;
            }}
            .highlight .mh {{
                color: #ae81ff;
            }}
            .highlight .mi {{
                color: #ae81ff;
            }}
            .highlight .mo {{
                color: #ae81ff;
            }}
            .highlight .sb {{
                color: #e6db74;
            }}
            .highlight .sc {{
                color: #e6db74;
            }}
            .highlight .sd {{
                color: #e6db74;
            }}
            .highlight .s2 {{
                color: #e6db74;
            }}
            .highlight .se {{
                color: #ae81ff;
            }}
            .highlight .sh {{
                color: #e6db74;
            }}
            .highlight .si {{
                color: #e6db74;
            }}
            .highlight .sx {{
                color: #e6db74;
            }}
            .highlight .sr {{
                color: #e6db74;
            }}
            .highlight .s1 {{
                color: #e6db74;
            }}
            .highlight .ss {{
                color: #e6db74;
            }}
            .highlight .bp {{
                color: #f8f8f2;
            }}
            .highlight .vc {{
                color: #f8f8f2;
            }}
            .highlight .vg {{
                color: #f8f8f2;
            }}
            .highlight .vi {{
                color: #f8f8f2;
            }}
            .highlight .il {{
                color: #ae81ff;
            }}
            blockquote {{
                border-left: 4px solid #3498db;
                margin: 1.5rem 0;
                padding: 0.5rem 1rem;
                background-color: #ebf5fb;
            }}
            hr {{
                border: none;
                border-top: 1px solid #e0e0e0;
                margin: 2rem 0;
            }}
            a {{
                color: #3498db;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        {markdown2.markdown(md_content, extras=['fenced-code-blocks', 'tables'])}
    </body>
    </html>
    """
    
    # Обрабатываем блоки кода для подсветки синтаксиса
    code_block_pattern = r'<pre><code class="language-(\w+)">(.*?)</code></pre>'
    def replace_code_block(match):
        language = match.group(1)
        code = match.group(2)
        try:
            lexer = get_lexer_by_name(language)
            formatter = HtmlFormatter(style='monokai')
            highlighted_code = highlight(code.strip(), lexer, formatter)
            return f'<div class="highlight">{highlighted_code}</div>'
        except:
            return f'<pre><code>{html.escape(code.strip())}</code></pre>'
    
    html_content = re.sub(code_block_pattern, replace_code_block, html_content, flags=re.DOTALL)
    
    # Сохраняем HTML файл
    html_file_path = md_file_path.replace('.md', '.html')
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return html_file_path

def open_theory_in_browser():
    """Создает HTML файл с теорией и открывает его в браузере"""
    # Создаем Markdown файл
    md_file_path = create_full_theory_markdown()
    
    # Конвертируем в HTML
    html_file_path = convert_md_to_html(md_file_path)
    
    # Получаем абсолютный путь к файлу
    abs_path = os.path.abspath(html_file_path)
    
    # Открываем в браузере
    webbrowser.open('file://' + abs_path)
    
    # Удаляем Markdown файл, так как он больше не нужен
    os.unlink(md_file_path) 