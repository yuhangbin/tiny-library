package com.cboy.library.task;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

@SpringBootTest
public class BookETLTaskTest {

    @Autowired
    BookETLTask bookETLTask;

    @Autowired
    VectorStore vectorStore;

    @Test
    void testRead() {
        List<Document> documents = bookETLTask.read();
        Assertions.assertFalse(documents.isEmpty());
    }

    @Test
    void testETL() {
        bookETLTask.ETL();
        List<Document> documents = vectorStore.similaritySearch("What is Pod?");
        Assertions.assertNotNull(documents);
    }
}
