import base64
from flask import Flask, render_template, request
from selenium_logic import search_company

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    title = None
    content = None
    tags = None

    if request.method == "POST":
        company = request.form["company"]
        company_decoration = request.form["company_decoration"]

        company_color = request.form["company_color"]

        color1 = request.form["color1"]
        color2 = request.form["color2"]
        color3 = request.form["color3"]
        color4 = request.form["color4"]
        colors = [color1, color2, color3, color4]

        footer_color = request.form["footer_color"]

        company_logo_b64 = None
        if "company_logo" in request.files:
            file = request.files["company_logo"]
            if file and file.filename != "":
                company_logo_b64 = base64.b64encode(file.read()).decode("utf-8")

        results = search_company(
            company,
            company_decoration,
            company_color,
            colors,
            footer_color,
            company_logo_b64,
        )

        UNIV_NAME_MAP = {
            "한국과학기술원": "KAIST",
            "포항공과대학교": "POSTECH",
            "대구경북과학기술원": "DIGIST",
            "광주과학기술원": "GIST",
            "울산과학기술원": "UNIST",
        }

        TAG_NAME_MAP = {
            "서울대학교": "서울대",
            "연세대학교": "연세대",
            "고려대학교": "고려대",
            "서강대학교": "서강대",
            "성균관대학교": "성균관대",
            "한양대학교": "한양대",
            "중앙대학교": "중앙대",
            "경희대학교": "경희대",
            "한국외국어대학교": "외대",
            "서울시립대학교": "시립대",
            "이화여자대학교": "이화여대",
            "건국대학교": "건국대",
            "동국대학교": "동국대",
            "홍익대학교": "홍익대",
            "국민대학교": "국민대",
            "숭실대학교": "숭실대",
            "세종대학교": "세종대",
            "단국대학교": "단국대",
            "광운대학교": "광운대",
            "명지대학교": "명지대",
            "상명대학교": "상명대",
            "가천대학교": "가천대",
            "인하대학교": "인하대",
            "아주대학교": "아주대",
            "서울과학기술대학교": "과기대",
            "부산대학교": "부산대",
            "경북대학교": "경북대",
            "인천대학교": "인천대",
            "충남대학교": "충남대",
            "전남대학교": "전남대",
            "충북대학교": "충북대",
            "KAIST": "카이스트",
            "POSTECH": "포스텍",
            "DIGIST": "디지스트",
            "GIST": "지스트",
            "UNIST": "유니스트",
        }

        tags = []

        if results:
            school_names = [school for school, _ in results]
            school_names = [UNIV_NAME_MAP.get(name, name) for name in school_names]
            for item in results:
                if isinstance(item, (list, tuple)):
                    school_names.append(str(item[0]))
                elif isinstance(item, dict):
                    school_names.append(item.get("school") or item.get("name") or str(item))
                else:
                    school_names.append(str(item))

            top4_str = ", ".join(school_names[:4])

            for name in school_names:
                tags.append(f"#{name.replace(' ', '')}")  # 원래 이름

                alias = TAG_NAME_MAP.get(name)
                if alias:
                    tags.append(f"#{alias.replace(' ', '')}")

            all_tags_str = " ".join(tags)

            title = f'2026년 "{company_decoration}" 재직자 출신 대학 순위 TOP10 한눈에 정리'

            content = (
                f"안녕하세요.\n"
                f"2026년 {company_decoration} 재직자 출신 대학 순위 TOP10이 공개되었습니다.\n"
                f'2026년 {company_decoration} 재직자 출신 대학 순위 에서는 {top4_str} 등 주요 대학들이 상위권에 이름을 올렸는데요.\n'
                f"입시를 준비하는 수험생들이나 대학 선택을 고민하는 학생들이라면 한 번쯤 참고해볼 만한 자료입니다."
            )

            tags = f"#대학순위 {all_tags_str}"

    return render_template(
        "index.html",
        results=results,
        title=title,
        content=content,
        tags=tags
    )


if __name__ == "__main__":
    app.run(debug=True)
