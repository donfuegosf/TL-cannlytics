// Cannlytics App
// Copyright (c) 2023 Cannlytics

// Authors:
//   Keegan Skeate <https://github.com/keeganskeate>
// Created: 2/20/2023
// Updated: 3/5/2023
// License: MIT License <https://github.com/cannlytics/cannlytics/blob/main/LICENSE>

// Dart imports:
import 'dart:convert';

// Package imports:
import 'package:firebase_auth/firebase_auth.dart';
import 'package:http/http.dart' as http;

/// Service to interface with the Cannlytics API.
class APIService {
  // Production / test base URL.
  // static final String baseUrl = 'https://cannlytics.com/api';
  static final String baseUrl = 'http://127.0.0.1:8000/api';

  /// Get a user's token. Set [refresh] to renew credentials.
  static Future<String> getUserToken({bool refresh = false}) async {
    final tokenResult = FirebaseAuth.instance.currentUser;
    if (tokenResult == null) return '';
    return await tokenResult.getIdToken(refresh);
  }

  /// Make an authenticated HTTP request to the Cannlytics API.
  static Future<dynamic> apiRequest(String endpoint,
      {dynamic data, Map<String, dynamic>? options}) async {
    // Create default body, method, and headers.
    var body;
    var method = 'GET';
    final idToken = await getUserToken();
    final headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $idToken',
    };

    // Handle post.
    if (data != null) {
      method = 'POST';
      body = jsonEncode(data);
    }

    // Handle options.
    if (options != null) {
      // Handle delete.
      if (options['delete'] == true) {
        method = 'DELETE';
      }

      // Handle query parameters.
      if (options['params'] != null) {
        final url = Uri.parse(endpoint);
        final newUrl = url.replace(queryParameters: options['params']);
        endpoint = newUrl.toString();
      }
    }

    // Format the URL
    final url = endpoint.startsWith(baseUrl) ? endpoint : '$baseUrl$endpoint';

    // Make the request.
    final client = http.Client();
    final request;
    if (body == null) {
      request = http.Request(method, Uri.parse(url))..headers.addAll(headers);
    } else {
      request = http.Request(method, Uri.parse(url))
        ..headers.addAll(headers)
        ..body = body;
    }

    // Get the response.
    final response = await client.send(request).then(http.Response.fromStream);

    // Return the data.
    try {
      var responseData = jsonDecode(response.body);
      return responseData.containsKey('data')
          ? responseData['data']
          : responseData;
    } catch (error) {
      return response;
    }
  }
}
