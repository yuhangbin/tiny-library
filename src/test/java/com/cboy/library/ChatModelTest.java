package com.cboy.library;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.DefaultChatClient;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.document.Document;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;
import java.util.stream.Collectors;

@SpringBootTest
public class ChatModelTest {

    @Autowired
    ChatClient chatClient;


    @Test
    void testChatModel() {

        String result = chatClient.prompt()
                .system("You are so smart")
                .user("tell me a joke")
                .call()
                .content();

        System.out.println(result);
        Assertions.assertNotNull(result);
    }
}
