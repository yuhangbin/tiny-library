package com.cboy.library;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

@SpringBootTest
public class VectorStoreTest {

    @Autowired
    VectorStore vectorStore;

    @Test
    void testAdd() {
        vectorStore.add(List.of(new Document("hello world")));
        List<Document> documents = vectorStore.similaritySearch("world");
        Assertions.assertNotNull(documents);
    }
}
