package com.cboy.library.config;

import io.micrometer.observation.ObservationRegistry;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.ollama.OllamaChatModel;
import org.springframework.ai.ollama.OllamaEmbeddingModel;
import org.springframework.ai.ollama.api.OllamaApi;
import org.springframework.ai.ollama.api.OllamaModel;
import org.springframework.ai.ollama.api.OllamaOptions;
import org.springframework.ai.ollama.management.ModelManagementOptions;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.vectorstore.pgvector.PgVectorStore;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;

@Configuration
public class ModelConfig {

    OllamaApi ollamaApi = new OllamaApi();


    @Bean
    public ChatClient chatClient() {
        return ChatClient.builder(OllamaChatModel.builder()
                .ollamaApi(ollamaApi)
                .defaultOptions(OllamaOptions.builder().model(OllamaModel.MISTRAL.id()).build())
                .build()).build();
    }

    @Bean
    public EmbeddingModel embeddingModel() {
        return new OllamaEmbeddingModel(ollamaApi,
                OllamaOptions.builder()
                        .model(OllamaModel.NOMIC_EMBED_TEXT.id())
                        .build(), ObservationRegistry.NOOP, ModelManagementOptions.defaults());
    }

    @Bean
    public VectorStore vectorStore(JdbcTemplate jdbcTemplate, EmbeddingModel embeddingModel) {
        return PgVectorStore.builder(jdbcTemplate, embeddingModel)
                // TODO check embedding model dimensions limit ( NOMIC_EMBED_TEXT limit is 768)
                .dimensions(1536)
                .distanceType(PgVectorStore.PgDistanceType.COSINE_DISTANCE)
                .indexType(PgVectorStore.PgIndexType.HNSW)
                .initializeSchema(false)
                .maxDocumentBatchSize(10000)
                .build();
    }

}
