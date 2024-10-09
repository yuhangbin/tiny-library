package com.cboy.library.resource;

import com.cboy.library.pojo.BookMetaData;

import java.util.Set;

public interface Book {

    BookMetaData get();

    String summary();

    Set<Book> similaritySearch();
}
