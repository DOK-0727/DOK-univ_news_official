import base64
from flask import Flask, render_template, request
from selenium_logic import search_company

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        company = request.form["company"]
        company_decoration = request.form["company_decoration"]

        company_color = request.form["company_color"]

        color1 = request.form["color1"]
        color2 = request.form["color2"]
        color3 = request.form["color3"]
        color4 = request.form["color4"]
        colors = [color1, color2, color3,color4]

        footer_color = request.form["footer_color"]

        # search_company 함수에 이미지 관련 인자 추가 전달
        results = search_company(company, company_decoration, company_color, colors, footer_color)

    return render_template(
        "index.html",
        results=results
    )

if __name__ == "__main__":
    app.run(debug=True)