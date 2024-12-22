package com.cboy.library.task;

import org.springframework.ai.document.Document;
import org.springframework.ai.reader.ExtractedTextFormatter;
import org.springframework.ai.reader.pdf.PagePdfDocumentReader;
import org.springframework.ai.reader.pdf.config.PdfDocumentReaderConfig;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class BookETLTask {

    @Autowired
    VectorStore vectorStore;

    public void ETL() {
        // read a book (such as: 'k8s in action')
        // spilt this book into many segments
        List<Document> bookSegments = read();
        // embedding segments (don't know how it works)
        // store into vector database
        vectorStore.add(bookSegments);
    }

    public List<Document> read() {
        PagePdfDocumentReader pdfReader = new PagePdfDocumentReader("classpath:books/Kubernetes in Action.pdf",
                PdfDocumentReaderConfig.builder()
                        .withPageTopMargin(0)
                        .withPageExtractedTextFormatter(ExtractedTextFormatter.builder()
                                .withNumberOfTopTextLinesToDelete(0)
                                .build())
                        .build());
        return pdfReader.read();
    }

    public List<Document> tokenize(List<Document> documents) {
        return documents;
    }


}
