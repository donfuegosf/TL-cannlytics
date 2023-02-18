// Cannlytics App
// Copyright (c) 2023 Cannlytics

// Authors:
//   Keegan Skeate <https://github.com/keeganskeate>
// Created: 2/18/2023
// Updated: 2/18/2023
// License: MIT License <https://github.com/cannlytics/cannlytics/blob/main/LICENSE>
import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:cannlytics_app/services/firebase_auth_repository.dart';
import 'package:cannlytics_app/services/firestore_repository.dart';
import 'package:cannlytics_app/models/job.dart';
import 'package:cannlytics_app/ui/edit_job_screen/job_submit_exception.dart';

class EditJobScreenController extends AutoDisposeAsyncNotifier<void> {
  @override
  FutureOr<void> build() {
    // ok to leave this empty if the return type is FutureOr<void>
  }

  Future<bool> submit(
      {Job? job, required String name, required int ratePerHour}) async {
    final currentUser = ref.read(authRepositoryProvider).currentUser;
    if (currentUser == null) {
      throw AssertionError('User can\'t be null');
    }
    // set loading state
    state = const AsyncLoading().copyWithPrevious(state);
    // check if name is already in use
    final database = ref.read(databaseProvider);
    final jobs = await database.fetchJobs(uid: currentUser.uid);
    final allLowerCaseNames =
        jobs.map((job) => job.name.toLowerCase()).toList();
    if (job != null) {
      allLowerCaseNames.remove(job.name.toLowerCase());
    }
    // check if name is already used
    if (allLowerCaseNames.contains(name.toLowerCase())) {
      state = AsyncError(JobSubmitException(), StackTrace.current);
      return false;
    } else {
      final id = job?.id ?? documentIdFromCurrentDate();
      final updated = Job(id: id, name: name, ratePerHour: ratePerHour);
      state = await AsyncValue.guard(
        () => database.setJob(uid: currentUser.uid, job: updated),
      );
      return state.hasError == false;
    }
  }
}

final editJobScreenControllerProvider =
    AutoDisposeAsyncNotifierProvider<EditJobScreenController, void>(
        EditJobScreenController.new);
