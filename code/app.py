import base64
from flask import Flask, render_template, request
from linkedin_download import search_company

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
                company_logo_b64 = base64.b64encode(
                    file.read()
                ).decode("utf-8")

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
            "대구경북과학기술원": "DGIST",
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
            "DGIST": "디지스트",
            "GIST": "지스트",
            "UNIST": "유니스트",
        }

        tags = []

        if results:

            cleaned_results = []

            for item in results:

                school = None
                count = None

                if isinstance(item, (list, tuple)):

                    if len(item) >= 2:
                        school = item[0]
                        count = item[1]

                elif isinstance(item, dict):

                    school = (
                            item.get("school")
                            or item.get("university")
                            or item.get("name")
                    )

                    count = (
                            item.get("count")
                            or item.get("people")
                            or item.get("number")
                    )

                else:
                    school = str(item)
                    count = 0

                if not school:
                    continue

                school = UNIV_NAME_MAP.get(
                    str(school),
                    str(school)
                )

                try:
                    count = int(count)
                except (ValueError, TypeError):
                    count = 0

                cleaned_results.append(
                    (school, count)
                )

            cleaned_results.sort(
                key=lambda x: x[1],
                reverse=True
            )

            top10_results = cleaned_results[:10]

            top4_str = ", ".join(
                school
                for school, count in top10_results[:4]
            )

            ranking_text = ""

            for rank, (school, count) in enumerate(
                    top10_results,
                    start=1
            ):
                ranking_text += (
                    f"{rank}위 {school} - {count}명\n"
                )

            title = (
                f"2026년 {company_decoration} "
                f"재직자 출신 대학 순위 TOP10 한눈에 정리"
            )

            content = (
                f"안녕하세요.\n\n"

                f"오늘은 2026년 {company_decoration} "
                f"재직자 출신 대학 순위 TOP10을 "
                f"정리해보겠습니다.\n\n"

                f"{company_decoration}에는 어떤 대학 출신의 "
                f"재직자가 많이 근무하고 있을까요?\n\n"

                f"이번 자료에서는 {company_decoration} "
                f"재직자의 출신 대학 데이터를 바탕으로 "
                f"인원이 많은 대학을 순위별로 정리했습니다. "
                f"{company_decoration} 취업을 준비하고 있는 "
                f"취업준비생이나 대학생, 해당 기업에 관심이 "
                f"있는 분들이라면 참고해볼 만한 자료입니다.\n\n"

                f"2026년 {company_decoration} "
                f"출신 대학 순위 TOP10을 살펴보겠습니다.\n\n"

                f"이번 조사에서 확인된 "
                f"{company_decoration} 재직자 출신 대학 TOP10은 "
                f"다음과 같습니다.\n\n"

                f"{ranking_text}\n"

                f"상위권에는 {top4_str} 등이 이름을 올렸으며, "
                f"그 외에도 다양한 대학 출신의 재직자가 "
                f"확인되었습니다.\n\n"

                f"이처럼 {company_decoration} 출신 대학 순위를 "
                f"살펴보면 해당 기업에서 어떤 대학 출신의 "
                f"재직자가 상대적으로 많이 확인되는지 "
                f"한눈에 확인할 수 있습니다.\n\n"

                f"단순히 대학 순위만 살펴보는 것뿐만 아니라, "
                f"어떤 대학 출신의 인원이 많은지, 주요 기업의 "
                f"재직자들은 어떤 대학을 졸업했는지를 "
                f"살펴볼 수 있다는 점에서도 흥미로운 자료입니다.\n\n"

                f"특히 {company_decoration} 취업을 준비하고 있는 "
                f"취업준비생이나 대학생이라면 기업 취업과 "
                f"관련된 참고 자료로 활용해볼 수 있습니다.\n\n"

                f"다만 출신 대학 순위가 취업 가능성을 의미하는 "
                f"것은 아닙니다. 실제 채용 과정에서는 학력뿐만 "
                f"아니라 직무 역량, 전공, 경력, 자격증, 인턴 및 "
                f"대외활동 등 다양한 요소가 종합적으로 고려될 "
                f"수 있습니다.\n\n"

                f"또한 이번 자료는 LinkedIn에서 확인한 데이터를 "
                f"바탕으로 정리한 자료이므로 "
                f"{company_decoration} 전체 임직원의 실제 "
                f"출신 대학 분포와는 차이가 있을 수 있습니다. "
                f"따라서 기업에서 공식적으로 발표한 통계나 "
                f"절대적인 대학 순위라기보다는 참고용 자료로 "
                f"봐주시기 바랍니다.\n\n"

                f"앞으로도 다양한 기업의 재직자 출신 대학, "
                f"기업별 대학 순위, 주요 기업 취업 관련 자료를 "
                f"정리해서 소개해드리겠습니다.\n\n"

                f"{company_decoration} 취업에 관심이 있거나 "
                f"기업별 출신 대학 순위, 대기업 취업, "
                f"금융권 취업, IT기업 취업 등의 정보를 찾고 "
                f"있다면 다른 기업의 출신 대학 순위도 "
                f"함께 확인해보세요."
            )

            school_names = [
                school
                for school, _ in results
            ]

            school_names = [
                UNIV_NAME_MAP.get(
                    name,
                    name
                )
                for name in school_names
            ]

            for item in results:

                if isinstance(item, (list, tuple)):

                    school_names.append(
                        str(item[0])
                    )

                elif isinstance(item, dict):

                    school_names.append(
                        item.get("school")
                        or item.get("name")
                        or str(item)
                    )

                else:

                    school_names.append(
                        str(item)
                    )

            top4_str = ", ".join(
                school_names[:4]
            )

            for name in school_names:

                tags.append(
                    f"#{name.replace(' ', '')}"
                )

                alias = TAG_NAME_MAP.get(name)

                if alias:
                    tags.append(
                        f"#{alias.replace(' ', '')}"
                    )

            all_tags_str = " ".join(tags)

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
