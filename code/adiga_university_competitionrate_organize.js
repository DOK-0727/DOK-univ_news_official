function doPost(e) {
    Logger.log(e.postData.contents);
    const data = JSON.parse(e.postData.contents);

    // Python(adiga_dept_download.py)에서 전달받는 인자 (색상 및 로고 제외)
    const department = data.department;
    const year = data.adiga_year;
    const admissionType = data.admission_type;
    const results = data.results;

    // 고정 색상 설정 (기존에는 Python에서 받았으나 이제 기본값 사용)
    const mainColor = "#000000";
    const headerColors = ['#000000', '#000000', '#000000', '#000000'];
    const footerColor = '#000000';
    const defaultColor = '#000000';

    // 대학별 브랜드 메인 색상 Map
    const schoolColorMap = {
        "서울대학교": "#1a3881",
        "연세대학교": "#003876",
        "고려대학교": "#7b0018",
        "서강대학교": "#b30000",
        "성균관대학교": "#76b71b",
        "한양대학교": "#0a4f92",
        "중앙대학교": "#2456a4",
        "경희대학교": "#9c1714",
        "한국외국어대학교": "#218190",
        "서울시립대학교": "#004094",
        "이화여자대학교": "#155421",
        "건국대학교": "#4b965e",
        "동국대학교": "#f7901f",
        "홍익대학교": "#000000",
        "국민대학교": "#00218c",
        "숭실대학교": "#0fa2cb",
        "세종대학교": "#c40224",
        "단국대학교": "#004d99",
        "광운대학교": "#850a03",
        "명지대학교": "#000066",
        "상명대학교": "#292267",
        "가천대학교": "#004c95",
        "인하대학교": "#01baf2",
        "아주대학교": "#0b4199",
        "서울과학기술대학교": "#000000",
        "부산대학교": "#00117d",
        "경북대학교": "#bc003d",
        "인천대학교": "#005599",
        "충남대학교": "#0c4ca3",
        "전남대학교": "#018635",
        "충북대학교": "#b92655",
        "한국과학기술원": "#004294",
        "포항공과대학교": "#c90060",
        "대구경북과학기술원": "#149fe8",
        "광주과학기술원": "#dc2715",
        "울산과학기술원": "#001655",
        "default": "#000000"
    };

    // 표기 약어 Map
    const schoolNameAliasMap = {
        "한국과학기술원": "KAIST",
        "포항공과대학교": "POSTECH",
        "대구경북과학기술원": "DGIST",
        "광주과학기술원": "GIST",
        "울산과학기술원": "UNIST"
    };

    // 대학 로고 URL Map
    const schoolLogoMap = {
        "서울대학교": "https://drive.google.com/uc?export=view&id=1Q-bswUPaZ0I-SUq9Hzx7UmhcFsjefByw",
        "연세대학교": "https://drive.google.com/uc?export=view&id=19afzCFS_qXorX-jFwNdDKjzW11wA-r0I",
        "고려대학교": "https://drive.google.com/uc?export=view&id=1uWjyQcdMHkwTtnoackxi7IEeJ7RmRhDC",
        "서강대학교": "https://drive.google.com/uc?export=view&id=1696A_pPejmhjpVfJQIPodFwT17cKC-tT",
        "성균관대학교": "https://drive.google.com/uc?export=view&id=1TLy-NjDVDbS22A-KbCh8QoQ7S2QpLLk0",
        "한양대학교": "https://drive.google.com/uc?export=view&id=15wbuMi95IjPKCFmPYlL_3-IyDuqo8B3I",
        "중앙대학교": "https://drive.google.com/uc?export=view&id=18U9NdrF-nZQtRtR3vM0NjqKwA9cjMGmb",
        "경희대학교": "https://drive.google.com/uc?export=view&id=1uGot1ye4CmPXWEeSNt_MrWbJbGK6eh7B",
        "한국외국어대학교": "https://drive.google.com/uc?export=view&id=1bM_CnRy6MHCpH6Ma74CE9tFwtWSKC4vB",
        "서울시립대학교": "https://drive.google.com/uc?export=view&id=1u_hrscHpHadBnLrhuhmNgAJxL9wMr7ey",
        "이화여자대학교": "https://drive.google.com/uc?export=view&id=1u5BbmbwmpKVUBrZvQjcsqFJ6CNOKzB5C",
        "건국대학교": "https://drive.google.com/uc?export=view&id=1H851xig2MLXXuByjjYbI-uRLblUjVqWq",
        "동국대학교": "https://drive.google.com/uc?export=view&id=10H6DGYa-bNEwgXvnHt_x5owWO9SkTTc7",
        "홍익대학교": "https://drive.google.com/uc?export=view&id=1EJXwv3TGgF5dRLCTSsz1KLDCgbJkbMVM",
        "국민대학교": "https://drive.google.com/uc?export=view&id=1k7HHV6MxMs6IfpTxnQ3L9I6t4fEOfZWT",
        "숭실대학교": "https://drive.google.com/uc?export=view&id=15BQviQnk71_KkWKe3rjXUjfdskRxeD_G",
        "세종대학교": "https://drive.google.com/uc?export=view&id=1DamVW-Lka44KTDEPJ93GIlEgDYe8Lr61",
        "단국대학교": "https://drive.google.com/uc?export=view&id=1RmzYpgXlJgqrc2x8QvaPPuqiapc3_gdv",
        "광운대학교": "https://drive.google.com/uc?export=view&id=1d-HmYFziFDBAMUla34dcfOsxzW0IgAgH",
        "명지대학교": "https://drive.google.com/uc?export=view&id=1dSz_v_Fa176JkJf8MDxhfcJEKSICFgqF",
        "상명대학교": "https://drive.google.com/uc?export=view&id=16hqaRpfYd_4HPah_4GeIDWb07yreQkhK",
        "가천대학교": "https://drive.google.com/uc?export=view&id=1RCJtD4rJRtD1ZaxS19LJWpCDu71yKcaI",
        "인하대학교": "https://drive.google.com/uc?export=view&id=1hODa-r6VIeAWF8EikG0J7xeEDz0Jx92u",
        "아주대학교": "https://drive.google.com/uc?export=view&id=1y59q4_VOfjzmqzGeNoQy3JMV01vF1585",
        "서울과학기술대학교": "https://drive.google.com/uc?export=view&id=1oGAGuN9ZCCQVtqyrZ5zMJJiQrY0M9aAn",
        "부산대학교": "https://drive.google.com/uc?export=view&id=1flaXUrw_4sttT4wSnlhoj1Ko5LyXGQwp",
        "경북대학교": "https://drive.google.com/uc?export=view&id=1qRgKp8VaWNzr2eLo_V4eX7cJU7ok0gTT",
        "인천대학교": "https://drive.google.com/uc?export=view&id=1zzO0RXPhEcS5PlL-JW7M7pKX9-KOF7Cx",
        "충남대학교": "https://drive.google.com/uc?export=view&id=140W1rSDTGawxRoQRRWLIN6qOZHH2zroa",
        "전남대학교": "https://drive.google.com/uc?export=view&id=15BUmPhnkBTZzvITyoubO2jBSh2-J8DWe",
        "충북대학교": "https://drive.google.com/uc?export=view&id=1bGLotsdDO3EgWaYs-8GK0iemsvXKBNJ0",
        "한국과학기술원": "https://drive.google.com/uc?export=view&id=12bD9_WXTFwnlArbUNTzJ6ccUovZUIoN8",
        "포항공과대학교": "https://drive.google.com/uc?export=view&id=18ePK3o9bfSXJQmxnUVjTuBUGOrpMbHvi",
        "대구경북과학기술원": "https://drive.google.com/uc?export=view&id=1XQJ-BtzdhpXT247Umb4WPZ9UexiqNidp",
        "광주과학기술원": "https://drive.google.com/uc?export=view&id=1Lofm2-QlecWQ3jcADlTtShMEayLuvD8g",
        "울산과학기술원": "https://drive.google.com/uc?export=view&id=1CqjejLpe16gCpQ8Ruv11FCB0oQdAeHl9"
    };

    // 1. Google 문서 생성
    const docTitle = year + "년 " + department + " " + admissionType + " 경쟁률 대학 순위 TOP10";
    const doc = DocumentApp.create(docTitle);
    const body = doc.getBody();

    const logoParagraph = body.getParagraphs()[0];

    // 3. 문서 대제목 (부제목) 구성: [연도]년 [학과명] [수시or정시] 경쟁률\n대학 순위 TOP10
    const subTitle = body.appendParagraph("");
    subTitle.setAlignment(DocumentApp.HorizontalAlignment.CENTER);

    subTitle.appendText(year + "년 ")
        .setBold(true)
        .setFontSize(35)
        .setForegroundColor(defaultColor);

    subTitle.appendText(department)
        .setBold(true)
        .setFontSize(35)
        .setForegroundColor(mainColor);

    subTitle.appendText("\n" + admissionType + " 경쟁률 대학 순위 TOP10")
        .setBold(true)
        .setFontSize(35)
        .setForegroundColor(defaultColor);

    const gap = body.appendParagraph(" ");
    gap.setFontSize(11);
    gap.setSpacingBefore(0);
    gap.setSpacingAfter(0);

    // 4. 표 데이터 구성
    const tableData = [];
    tableData.push(["순위", "", "학교명", "경쟁률"]);

    results.forEach(function (item, index) {
        let rank = String(index + 1);
        let originalSchoolName = item[0];
        let displaySchoolName = schoolNameAliasMap[originalSchoolName] || originalSchoolName;
        let rate = String(item[1]);

        tableData.push([rank, "", displaySchoolName, rate]);
    });

    const table = body.appendTable(tableData);

    // 5. 표 헤더 스타일 적용
    const headerRow = table.getRow(0);
    for (let i = 0; i < headerRow.getNumCells(); i++) {
        let cell = headerRow.getCell(i);
        if (headerColors[i]) {
            cell.setBackgroundColor(headerColors[i]);
        }
        let p = cell.getChild(0).asParagraph();
        p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);

        let text = cell.editAsText();
        text.setForegroundColor('#FFFFFF');
        text.setBold(true);
        text.setFontSize(12);
    }

    // 6. 데이터 행 스타일 및 텍스트 적용
    for (let r = 1; r < table.getNumRows(); r++) {
        let row = table.getRow(r);
        let dataIndex = r - 1;
        let originalSchoolName = results[dataIndex][0];

        for (let c = 0; c < row.getNumCells(); c++) {
            let cell = row.getCell(c);
            let p = cell.getChild(0).asParagraph();

            if (c === 1) {
                p.setAlignment(DocumentApp.HorizontalAlignment.RIGHT);
            } else if (c === 2) {
                p.setAlignment(DocumentApp.HorizontalAlignment.LEFT);
                p.setSpacingBefore(10);
            } else {
                p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
                p.setSpacingBefore(10);
            }

            let cellText = cell.editAsText();
            cellText.setFontSize(12);
            cellText.setBold(true);

            // 대학별 시그니처 색상 적용
            if (c === 2) {
                let targetColor = schoolColorMap[originalSchoolName] || schoolColorMap["default"];
                cellText.setForegroundColor(targetColor);
            }
        }
    }

    // 7. 각 대학 로고를 표 내부(2번째 열)에 추가
    for (let r = 1; r < table.getNumRows(); r++) {
        const row = table.getRow(r);
        const school = results[r - 1][0];
        const logoUrl = schoolLogoMap[school];

        if (!logoUrl) continue;

        try {
            const blob = UrlFetchApp.fetch(logoUrl).getBlob();
            const logoCell = row.getCell(1);

            while (logoCell.getNumChildren() > 0) {
                logoCell.removeChild(logoCell.getChild(0));
            }

            const p = logoCell.appendParagraph("");
            const inlineImage = p.appendInlineImage(blob);

            const origWidth = inlineImage.getWidth();
            const origHeight = inlineImage.getHeight();

            const targetHeight = 38;
            const targetWidth = Math.round((origWidth / origHeight) * targetHeight);

            inlineImage.setWidth(targetWidth);
            inlineImage.setHeight(targetHeight);

            p.setAlignment(DocumentApp.HorizontalAlignment.RIGHT);

        } catch (err) {
            Logger.log(school + " 로고 불러오기 실패: " + err);
        }
    }

    // 8. 하단 출처 표기
    const footer = body.getChild(body.getChildIndex(table) + 1).asParagraph();
    footer.setText("출처: 대입정보포털");
    footer.setAlignment(DocumentApp.HorizontalAlignment.LEFT);
    footer.setSpacingBefore(0);
    footer.setSpacingAfter(0);

    const footerTextObj = footer.editAsText();
    footerTextObj.setForegroundColor(footerColor);
    footerTextObj.setBold(true);
    footerTextObj.setFontSize(11);

    return ContentService.createTextOutput(doc.getUrl());
}