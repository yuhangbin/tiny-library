package com.cboy.library;

import io.micrometer.observation.ObservationRegistry;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.ai.embedding.*;
import org.springframework.ai.ollama.OllamaEmbeddingModel;
import org.springframework.ai.ollama.api.OllamaApi;
import org.springframework.ai.ollama.api.OllamaModel;
import org.springframework.ai.ollama.api.OllamaOptions;
import org.springframework.ai.ollama.management.ModelManagementOptions;

import java.util.List;

public class EmbeddingModelTest {

    @Test
    void testEmbeddingModel() {
        OllamaApi ollamaApi = new OllamaApi();
        EmbeddingModel embeddingModel = new OllamaEmbeddingModel(
                ollamaApi, OllamaOptions.builder()
                .model(OllamaModel.MISTRAL.id())
                .build(),
                ObservationRegistry.NOOP, ModelManagementOptions.defaults()
        );
        float[] embed = embeddingModel.embed("hello world");
        List<String> texts = List.of("hello world");
        EmbeddingRequest request = new EmbeddingRequest(texts, EmbeddingOptionsBuilder.builder().build());
        EmbeddingResponse response = embeddingModel.call(request);
        Assertions.assertFalse(response.getResults().isEmpty());
    }

    @Test
    void testEmbeddingModel_() {
        OllamaApi ollamaApi = new OllamaApi();
        EmbeddingModel embeddingModel = new OllamaEmbeddingModel(
                ollamaApi, OllamaOptions.builder()
                .model(OllamaModel.NOMIC_EMBED_TEXT.id())
                .build(),
                ObservationRegistry.NOOP, ModelManagementOptions.defaults()
        );
        float[] embed = embeddingModel.embed("hello world");
        Assertions.assertTrue(embed.length > 0);
    }
}
