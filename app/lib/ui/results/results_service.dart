// Cannlytics Data
// Copyright (c) 2023 Cannlytics

// Authors:
//   Keegan Skeate <https://github.com/keeganskeate>
// Created: 6/13/2023
// Updated: 9/5/2023
// License: MIT License <https://github.com/cannlytics/cannlytics/blob/main/LICENSE>

// Dart imports:
import 'dart:async';
// import 'package:async/async.dart' show StreamGroup;

// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Project imports:
import 'package:cannlytics_data/common/inputs/string_controller.dart';
import 'package:cannlytics_data/models/lab_result.dart';
import 'package:cannlytics_data/services/firestore_service.dart';
import 'package:cannlytics_data/services/storage_service.dart';
import 'package:cannlytics_data/ui/account/account_controller.dart';

/* === Data === */

// Date range.
final currentPageProvider = StateProvider<int>((ref) => 0);
final startDateProvider = StateProvider<DateTime?>((ref) {
  DateTime now = DateTime.now();
  return DateTime(now.year, now.month + 1, 0);
});
final endDateProvider = StateProvider<DateTime?>((ref) {
  DateTime now = DateTime.now();
  return DateTime(now.year, now.month - 3, 1);
});

/// Stream user results from Firebase.
final userResults = StreamProvider.autoDispose<List<Map?>>((ref) async* {
  final FirestoreService _dataSource = ref.watch(firestoreProvider);
  final user = ref.watch(userProvider).value;
  if (user == null) return;
  final startDate = ref.watch(startDateProvider);
  final endDate = ref.watch(endDateProvider);
  final snapshotStream = _dataSource.streamCollection(
    path: 'users/${user.uid}/lab_results',
    builder: (data, documentId) => data,
    queryBuilder: (query) {
      Query<Map<String, dynamic>> paginatedQuery = query
          .orderBy('coa_parsed_at', descending: true)
          .startAt([startDate?.toIso8601String()]).endAt(
              [endDate?.toIso8601String()]).limit(2000);
      return paginatedQuery;
    },
  );
  yield* snapshotStream;
});

/// Stream a user's lab results stats.
final userResultsStatsProvider = StreamProvider.autoDispose<Map?>((ref) {
  final _database = ref.watch(firestoreProvider);
  final user = ref.watch(userProvider).value;
  if (user == null) return Stream.value(null);
  return _database.streamDocument(
    path: 'users/${user.uid}/stats/lab_results',
    builder: (data, documentId) {
      return data ?? {};
    },
  );
});

/// Stream a result from Firebase.
final labResultProvider =
    StreamProvider.autoDispose.family<LabResult?, String>((ref, hash) {
  final _database = ref.watch(firestoreProvider);
  final user = ref.watch(userProvider).value;
  if (user == null) return Stream.value(null);
  return _database.streamDocument(
    path: 'users/${user.uid}/lab_results/$hash',
    builder: (data, documentId) {
      // Keep track of analysis results for editing.
      var labResult = LabResult.fromMap(data ?? {});
      var results =
          labResult.results?.map((result) => result?.toMap()).toList();
      ref.read(analysisResults.notifier).update((state) => results ?? []);
      ref.read(updatedLabResult.notifier).update((state) => labResult);
      return labResult;
    },
  );
});

/// Stream user's COA parsing jobs from Firebase.
/// FIXME: Exclude finished jobs with queries.
// final resultJobsProvider = StreamProvider.autoDispose<List<Map?>>((ref) async* {
//   final FirestoreService _dataSource = ref.watch(firestoreProvider);
//   final user = ref.watch(userProvider).value;
//   yield* Stream.value(<Map<dynamic, dynamic>?>[]);
//   if (user == null) return;
//   yield* _dataSource.streamCollection(
//     path: 'users/${user.uid}/parse_coa_jobs',
//     builder: (data, documentId) {
//       if (data?['job_finished'] == true && data?['job_error'] == false) {
//         return null;
//       }
//       return data;
//     },
//     queryBuilder: (query) =>
//         query.orderBy('job_created_at', descending: true).limit(1000),
//   );
// });
final resultJobsProvider = StreamProvider.autoDispose<List<Map?>>((ref) async* {
  final user = ref.watch(userProvider).value;
  yield* Stream.value(<Map<dynamic, dynamic>?>[]);
  if (user == null) return;
  var query = FirebaseFirestore.instance
      .collection('users/${user.uid}/parse_coa_jobs')
      .where(Filter.or(
        Filter('job_finished', isEqualTo: false),
        Filter('job_error', isEqualTo: true),
      ))
      .orderBy('job_created_at', descending: true)
      .limit(1000);
  yield* query
      .snapshots()
      .map((snapshot) => snapshot.docs.map((doc) => doc.data()).toList());
});

// Updated result.
final updatedLabResult = StateProvider<LabResult?>((ref) => null);

// Updated analysis results.
final analysisResults = StateProvider<List<Map?>>((ref) => []);

// New analysis result.
final newAnalysisResult = StateProvider<Map>((ref) => {});

// Result service provider.
final resultService = Provider<ResultService>((ref) {
  final uid = ref.read(userProvider).value?.uid ?? 'cannlytics';
  return ResultService(ref.watch(firestoreProvider), uid);
});

/// Result service.
class ResultService {
  const ResultService(this._dataSource, this.uid);

  // Parameters.
  final FirestoreService _dataSource;
  final String uid;

  // Update result.
  Future<void> updateResult(String id, Map<String, dynamic> data) async {
    await _dataSource.updateDocument(
      path: 'users/$uid/lab_results/$id',
      data: data,
    );
  }

  // Delete result.
  Future<void> deleteResult(String id) async {
    await _dataSource.deleteDocument(path: 'users/$uid/lab_results/$id');
  }
}

/* === Extraction === */

/// Parse COA data through the API.
class COAParser extends AsyncNotifier<List<Map?>> {
  /// Initialize the parser.
  @override
  Future<List<Map?>> build() async {
    // return await _loadUnfinishedJobs();
    return [];
  }

  // /// Load un-finished jobs.
  // Future<List<Map?>> _loadUnfinishedJobs() async {
  //   final user = ref.watch(userProvider).value;
  //   if (user == null) return [];
  //   var snapshot = await FirebaseFirestore.instance
  //       .collection('users')
  //       .doc(user.uid)
  //       .collection('parse_coa_jobs')
  //       .where('job_finished', isEqualTo: false)
  //       .get();

  //   return snapshot.docs.map((doc) => doc.data()).toList();
  // }

  /// Common method to create a job in Firestore and return data for it
  Future<Map<String, dynamic>> _createJob(
    String uid, {
    dynamic file,
    String? fileName,
    String? fileUrl,
  }) async {
    // Create a job document in Firestore.
    DocumentReference docRef = FirebaseFirestore.instance
        .collection('users')
        .doc(uid)
        .collection('parse_coa_jobs')
        .doc();
    String jobId = docRef.id;
    String fileRef = 'users/$uid/parse_coa_jobs/$jobId';

    // If there's a file, upload it to Firebase Storage and get the download URL.
    if (file != null) {
      await StorageService.uploadRawData(fileRef, file);
      fileUrl = await StorageService.getDownloadUrl(fileRef);
    }

    // Return the job data.
    return {
      'uid': uid,
      'job_id': jobId,
      'job_created_at': DateTime.now().toIso8601String(),
      'job_finished': false,
      'job_finished_at': null,
      'job_error': false,
      'job_error_message': null,
      'job_duration': 0,
      'job_file_ref': fileRef,
      'job_file_url': fileUrl,
      'job_file_name': fileName,
    };
  }

  /// Parse a COA from a URL.
  /// [✓]: TEST: https://portal.acslabcannabis.com/qr-coa-view?salt=QUFFSTM3N181NzU5NDAwMDQwMzA0NTVfMDQxNzIwMjNfNjQzZDhiOTcyMzE1YQ==
  Future<void> parseUrl(String fileUrl) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      var allData = state.value ?? [];
      final user = ref.watch(userProvider).value;
      if (user == null) return [];
      Map<String, dynamic> data = await _createJob(user.uid, fileUrl: fileUrl);
      allData.add(data);
      String docRef = 'users/${user.uid}/parse_coa_jobs/${data['job_id']}';
      await ref
          .read(firestoreProvider)
          .updateDocument(path: docRef, data: data);
      return allData;
    });
  }

  /// Parse COA files (PDFs and images).
  Future<void> parseCOAs(
    List<dynamic> files, {
    List<dynamic>? fileNames,
  }) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      var allData = state.value ?? [];
      final user = ref.watch(userProvider).value;
      if (user == null) return [];
      for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var fileName =
            fileNames != null && fileNames.length > i ? fileNames[i] : null;
        Map<String, dynamic> data = await _createJob(
          user.uid,
          file: file,
          fileName: fileName,
        );
        allData.add(data);
        String docRef = 'users/${user.uid}/parse_coa_jobs/${data['job_id']}';
        await ref
            .read(firestoreProvider)
            .updateDocument(path: docRef, data: data);
      }
      return allData;
    });
  }

  /// Retry a job.
  Future<void> retryJob(String uid, String jobId) async {
    final FirestoreService firestoreService = ref.read(firestoreProvider);

    // Fetch the receipt's data from Firestore using its job_id.
    String docRef = 'users/$uid/parse_coa_jobs/$jobId';
    Map<String, dynamic>? data =
        await firestoreService.getDocument(path: docRef);
    if (data == null) {
      print('Error: Receipt data not found for job id: $jobId');
      return;
    }

    // Delete the existing document from Firestore.
    await deleteJob(uid, jobId);

    // Recreate the document in Firestore using the fetched data.
    DocumentReference newDocRef = FirebaseFirestore.instance
        .collection('users')
        .doc(uid)
        .collection('parse_coa_jobs')
        .doc();
    data['job_id'] = newDocRef.id;
    data['job_created_at'] = DateTime.now().toIso8601String();
    await firestoreService.updateDocument(path: newDocRef.path, data: data);

    // Optionally: Update the state if needed.
    state = AsyncValue.data((state.value ?? [])..add(data));
  }

  /// Delete a job.
  Future<void> deleteJob(String uid, String jobId) async {
    String docRef = 'users/$uid/parse_coa_jobs/$jobId';
    await ref.read(firestoreProvider).deleteDocument(path: docRef);
    state = AsyncValue.data(
        (state.value ?? [])..removeWhere((item) => item?['job_id'] == jobId));
  }

  // Clear parsing results.
  Future<void> clear() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      return [];
    });
  }
}

// An instance of the user results provider.
final coaParser = AsyncNotifierProvider<COAParser, List<Map?>>(() {
  return COAParser();
});

/* === Search === */

// TODO: Implement filters:
// - state
// - product_type

// COA URL search input.
final urlSearchController =
    StateNotifierProvider<StringController, TextEditingController>(
        (ref) => StringController());

// COA search term.
final resultsSearchTerm = StateProvider<String>((ref) => '');

// Lab results search input.
final resultsSearchController =
    StateNotifierProvider<StringController, TextEditingController>(
        (ref) => StringController());

// Keywords-only query.
final keywordsQuery = StateProvider<Query<LabResult>>((ref) {
  // Get a list of keywords from the search term.
  String searchTerm = ref.watch(resultsSearchTerm);
  List<String> keywords = searchTerm.toLowerCase().split(' ');

  // Query by keywords.
  return FirebaseFirestore.instance
      .collection('public/data/lab_results')
      .where('keywords', arrayContainsAny: keywords)
      .withConverter(
        fromFirestore: (snapshot, _) => LabResult.fromMap(snapshot.data()!),
        toFirestore: (LabResult item, _) => item.toMap(),
      );
});

/* === Logs === */

// Result edit history logs.
final resultLogs = StateProvider.family<Query<Map<dynamic, dynamic>?>, String>((
  ref,
  sampleId,
) {
  return FirebaseFirestore.instance
      .collection('public/data/lab_results/$sampleId/lab_result_logs')
      .orderBy('created_at', descending: true)
      .withConverter(
        fromFirestore: (snapshot, _) => snapshot.data()!,
        toFirestore: (item, _) => item as Map<String, Object?>,
      );
});
