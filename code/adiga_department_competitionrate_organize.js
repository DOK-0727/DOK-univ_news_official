function doPost(e) {
    const data = JSON.parse(e.postData.contents);

    const university = data.university;
    const year = data.adiga_year;
    const admissionType = data.admissionType;
    const results = data.results;
    const univColor = data.univColor || "#000000";
    const headerColors = data.colors || ['#000000', '#000000', '#000000', '#000000'];
    const footerColor = data.footerColor || '#000000';
    const univLogo = data.univLogo;

    const docTitle = year + "년 " + university + " " + admissionType + " 경쟁률 순위 TOP10";
    const doc = DocumentApp.create(docTitle);
    const body = doc.getBody();

    const logoParagraph = body.getParagraphs()[0];
    if (univLogo) {
        try {
            const decoded = Utilities.base64Decode(univLogo);
            const logoBlob = Utilities.newBlob(decoded, 'image/png', 'univ_logo.png');
            const inlineImage = logoParagraph.appendInlineImage(logoBlob);

            const targetHeight = 76;
            const targetWidth = Math.round((inlineImage.getWidth() / inlineImage.getHeight()) * targetHeight);
            inlineImage.setWidth(targetWidth).setHeight(targetHeight);
            logoParagraph.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
        } catch (err) {
            logoParagraph.setText(university).setAlignment(DocumentApp.HorizontalAlignment.CENTER);
        }
    }

    const titlePara1 = body.appendParagraph("");
    titlePara1.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
    titlePara1.appendText(year + "년 ").setBold(true).setFontSize(35).setForegroundColor("#000000");
    titlePara1.appendText(university).setBold(true).setFontSize(35).setForegroundColor(univColor);

    const titlePara2 = body.appendParagraph(admissionType + " 경쟁률 순위 TOP10");
    titlePara2.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
    titlePara2.editAsText().setBold(true).setFontSize(35).setForegroundColor("#000000");

    const gap = body.appendParagraph(" ");
    gap.setFontSize(11).setSpacingBefore(0).setSpacingAfter(0);

    const tableData = [];
    tableData.push(["순위", "", "학과명", "경쟁률"]);

    results.forEach(function (item, index) {
        tableData.push([String(index + 1), "", item[0], String(item[1])]);
    });

    const table = body.appendTable(tableData);

    const headerRow = table.getRow(0);
    for (let i = 0; i < headerRow.getNumCells(); i++) {
        let cell = headerRow.getCell(i);
        if (headerColors[i]) cell.setBackgroundColor(headerColors[i]);
        let p = cell.getChild(0).asParagraph();
        p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
        let text = cell.editAsText();
        text.setForegroundColor('#FFFFFF').setBold(true).setFontSize(12);
    }

    for (let r = 1; r < table.getNumRows(); r++) {
        let row = table.getRow(r);
        for (let c = 0; c < row.getNumCells(); c++) {
            let cell = row.getCell(c);
            let p = cell.getChild(0).asParagraph();

            let cellText = cell.editAsText();
            cellText.setFontSize(12).setBold(true);

            if (c === 0 || c === 3) {
                p.setAlignment(DocumentApp.HorizontalAlignment.CENTER);
                p.setSpacingBefore(10);
                cellText.setForegroundColor("#000000");
            } else if (c === 2) {
                p.setAlignment(DocumentApp.HorizontalAlignment.LEFT);
                p.setSpacingBefore(10);
                cellText.setForegroundColor(univColor);
            }

            if (c === 1 && univLogo) {
                try {
                    while (cell.getNumChildren() > 0) cell.removeChild(cell.getChild(0));
                    const imgPara = cell.appendParagraph("");
                    const decoded = Utilities.base64Decode(univLogo);
                    const logoBlob = Utilities.newBlob(decoded, 'image/png', 'icon.png');
                    const inlineImage = imgPara.appendInlineImage(logoBlob);

                    const tHeight = 38;
                    const tWidth = Math.round((inlineImage.getWidth() / inlineImage.getHeight()) * tHeight);
                    inlineImage.setWidth(tWidth).setHeight(tHeight);
                    imgPara.setAlignment(DocumentApp.HorizontalAlignment.RIGHT);
                } catch (err) { }
            }
        }
    }

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