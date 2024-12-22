package com.cboy.library;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;
import java.util.stream.Collectors;

@SpringBootTest
public class RAGTest {

    final String q1 = "what's difference between pod and container in k8s?";

    @Autowired
    VectorStore vectorStore;

    @Autowired
    ChatClient chatClient;

    @Test
    void testQ1() {
        // search the vector store for the top 4 bikes that match the query
        SearchRequest request = SearchRequest.builder()
                .query(q1)
                .topK(2)
                .build();

        List<Document> topMatches = this.vectorStore.similaritySearch(request);

        // generate a response to the user's question based on the top matches
        String specs =
                topMatches.stream()
                        .map(document -> "\n===\n" + document.getContent() + "\n===\n")
                        .collect(Collectors.joining());

        String result = chatClient
                .prompt()
                .system(
                        """
                                You are a knowledgeable assistant that answers questions about books using provided context passages. Your role is to:
                                       - Answer questions based ONLY on the provided context, not external knowledge
                                       - If the context doesn't contain relevant information, say so honestly
                                       - Quote specific passages from the context when relevant
                                       - Maintain the author's voice and perspective
                                       - Don't reveal the RAG system mechanics to users
                                """)
                .user(
                        u ->
                                u.text(
                                                """
                                           Answer the question in <question></question> section based on the
                                           context in the <context></context> section
                        
                                           <question>
                                           {question}
                                           </question>
                        
                                           <context>
                                           {context}
                                           </context>
                                            """)
                                        .param("question", q1)
                                        .param("context", specs))
                .call()
                .content();
        System.out.println(result);
        Assertions.assertNotNull(result);
    }
}
