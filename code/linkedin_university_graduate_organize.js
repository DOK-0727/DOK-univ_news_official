function doPost(e) {
    Logger.log(e.postData.contents);
    const data = JSON.parse(e.postData.contents);

    const company = data.company;
    const companyDecoration = data.companyDecoration;
    const year = data.linkedin_year;
    const companyLogo = data.companyLogo;
    const results = data.results;
    const companyColor = data.companyColor || "#000000";
    const headerColors = data.colors || ['#000000', '#000000', '#000000', '#000000'];
    const footerColor = data.footerColor || '#000000';
    const defaultColor = '#000000';

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

    const schoolNameAliasMap = {
        "한국과학기술원": "KAIST",
        "포항공과대학교": "POSTECH",
        "대구경북과학기술원": "DGIST",
        "광주과학기술원": "GIST",
        "울산과학기술원": "UNIST"
    };

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

    const doc = DocumentApp.create(year + "년 " + companyDecoration + " 재직자 출신 대학 순위 TOP10");
    const body = doc.getBody();

    const logoParagraph = body.getParagraphs()[0];

    if (companyLogo) {
        try {
            const decoded = Utilities.base64Decode(companyLogo);
            const logoBlob = Utilities.newBlob(decoded, 'image/png', 'company_logo.png');

            const inlineImage = logoParagraph.appendInlineImage(logoBlob);

            const origWidth = inlineImage.getWidth();
            const origHeight = inlineImage.getHeight();

            const targetHeight = 76;
            const targetWidth = Math.round((origWidth / origHeight) * targetHeight);

            inlineImage.setWidth(targetWidth);
            inlineImage.setHeight(targetHeight);

            logoParagraph.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
        } catch (err) {
            Logger.log("로고 이미지 처리 실패: " + err);
            logoParagraph.setText(company);
            logoParagraph.setAlignment(DocumentApp.HorizontalAlignment.CENTER)
                .setHeading(DocumentApp.ParagraphHeading.HEADING1);
        }
    } else {
        logoParagraph.setText(company);
        logoParagraph.setAlignment(DocumentApp.HorizontalAlignment.CENTER)
            .setHeading(DocumentApp.ParagraphHeading.HEADING1);
    }

    const subTitle = body.appendParagraph("");
    subTitle.setAlignment(DocumentApp.HorizontalAlignment.CENTER);

    subTitle.appendText(year + "년 ")
        .setBold(true)
        .setFontSize(35)
        .setForegroundColor(defaultColor);

    subTitle.appendText(companyDecoration)
        .setBold(true)
        .setFontSize(35)
        .setForegroundColor(companyColor);

    subTitle.appendText(" 재직자\n출신 대학 순위 TOP10")
        .setBold(true)
        .setFontSize(35)
        .setForegroundColor(defaultColor);

    const gap = body.appendParagraph(" ");
    gap.setFontSize(11);
    gap.setSpacingBefore(0);
    gap.setSpacingAfter(0);

    const tableData = [];
    tableData.push(["순위", "", "학교명", "인원"]);

    results.forEach(function (item, index) {
        let rank = String(index + 1);
        let originalSchoolName = item[0];
        let displaySchoolName = schoolNameAliasMap[originalSchoolName] || originalSchoolName;
        let count = String(item[1]);

        tableData.push([rank, "", displaySchoolName, count + "명"]);
    });

    const table = body.appendTable(tableData);

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

            if (c === 2) {
                let targetColor =
                    schoolColorMap[originalSchoolName] || schoolColorMap["default"];
                cellText.setForegroundColor(targetColor);
            }
        }
    }

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
            Logger.log(school);
            Logger.log(err);
        }
    }

    const footer = body.getChild(body.getChildIndex(table) + 1).asParagraph();

    footer.setText("출처: LinkedIn");
    footer.setAlignment(DocumentApp.HorizontalAlignment.LEFT);
    footer.setSpacingBefore(0);
    footer.setSpacingAfter(0);

    const footerTextObj = footer.editAsText();
    footerTextObj.setForegroundColor(footerColor);
    footerTextObj.setBold(true);
    footerTextObj.setFontSize(11);

    return ContentService.createTextOutput(doc.getUrl());
}