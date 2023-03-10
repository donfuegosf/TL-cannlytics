// Cannlytics App
// Copyright (c) 2023 Cannlytics

// Authors:
//   Keegan Skeate <https://github.com/keeganskeate>
// Created: 3/3/2023
// Updated: 3/6/2023
// License: MIT License <https://github.com/cannlytics/cannlytics/blob/main/LICENSE>

// Dart imports:
import 'dart:async';

// Package imports:
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Project imports:
import 'package:cannlytics_app/models/common/organization.dart';
import 'package:cannlytics_app/services/api_service.dart';
import 'package:cannlytics_app/services/auth_service.dart';
import 'package:cannlytics_app/services/firestore_service.dart';

// Organizations controller.
final organizationsController =
    AutoDisposeAsyncNotifierProvider<OrganizationsController, void>(
        OrganizationsController.new);

/// Manage organizations.
class OrganizationsController extends AutoDisposeAsyncNotifier<void> {
  @override
  FutureOr<void> build() {}

  /// TODO: Create organization.
  Future<void> createOrganization() async {
    state = const AsyncValue.loading();
    // state = await AsyncValue.guard();
  }

  // TODO: Update organization.
  Future<void> updateOrganization() async {
    state = const AsyncValue.loading();
    // state = await AsyncValue.guard();
  }

  // TODO: Delete organization.
  Future<void> deleteOrganization() async {
    state = const AsyncValue.loading();
    // state = await AsyncValue.guard();
  }

  // TODO: Accept team member.
  Future<void> acceptTeamMember() async {
    state = const AsyncValue.loading();
    // state = await AsyncValue.guard();
  }

  // TODO: Invite team member.
  Future<void> inviteTeamMember() async {
    state = const AsyncValue.loading();
    // state = await AsyncValue.guard();
  }

  // TODO: Request to join an organization.
  Future<void> joinOrganization() async {
    state = const AsyncValue.loading();
    // state = await AsyncValue.guard();
  }
}


/* WORKING */

// // Organizations service provider.
// final organizationsServiceProvider = Provider<OrganizationsService>((ref) {
//   return OrganizationsService(ref.watch(firestoreProvider));
// });

// /// Organizations service.
// class OrganizationsService {
//   const OrganizationsService(this._dataSource);
//   final FirestoreService _dataSource;

//   Future<List<Organization>> getOrganizations() async {
//     List<Map> response = await APIService.apiRequest('/organizations');
//     print('RESPONSE:');
//     print(response);
//     return response.map((org) => Organization.fromMap(org)).toList();
//   }
// }

// /// Organizations stream.
// final organizationsProvider =
//     FutureProvider.autoDispose<List<Organization>>((ref) async {
//   final service = ref.watch(organizationsServiceProvider);
//   return await service.getOrganizations();
// });

// // Organization provider.
// final organizationProvider = StreamProvider.autoDispose<Map>((ref) {
//   final user = ref.watch(userProvider).value;
//   final _database = ref.watch(firestoreProvider);
//   // FIXME: Get the current organization ID.
//   final orgId = 'test-company';
//   print('CURRENT USER:');
//   print(user!.uid);
//   print('CURRENT ORGANIZATION:');
//   print(orgId);
//   return _database.watchDocument(
//     path: FirestorePath.organization(orgId),
//     builder: (data, documentId) {
//       return data ?? {};
//     },
//   );
// });

/* SCRAP */

// Organization licenses provider.
// final organizationsProvider = StreamProvider.autoDispose<Map>((ref) {
//   final user = ref.watch(userProvider).value;
//   final _database = ref.watch(firestoreProvider);
//   // Get the current organization ID.
//   final orgId = 'test-company';
//   print('CURRENT USER:');
//   print(user!.uid);
//   print('CURRENT ORGANIZATION:');
//   print(orgId);
//   return _database.watchDocument(
//     path: FirestorePath.organization(orgId),
//     builder: (data, documentId) {
//       return data ?? {};
//     },
//   );
// });

// // Organizations provider.
// final organizationsProvider =
//     AutoDisposeAsyncNotifierProvider<OrganizationsController, void>(
//         OrganizationsController.new);

// /// Organizations controller.
// class OrganizationsController extends AutoDisposeAsyncNotifier<void> {
//   @override
//   FutureOr<void> build() {}

//   /// Get organizations.
//   Future<List<Organization>> getOrganizations() async {
//     List<Map> response = await APIService.apiRequest('/organizations');
//     print('RESPONSE:');
//     print(response);
//     return response.map((org) => Organization.fromMap(org)).toList();
//   }
// }

// Organizations provider.
// final organizationsProvider = extends AutoDisposeAsyncNotifier<void> {
//   // final user = ref.watch(userProvider).value;
//   // final _database = ref.watch(firestoreProvider);
//   // // Get the current organization ID.
//   // final orgId = 'test-company';
//   // print('CURRENT USER:');
//   // print(user!.uid);
//   // print('CURRENT ORGANIZATION:');
//   // print(orgId);
//   // return _database.watchDocument(
//   //   path: FirestorePath.organization(orgId),
//   //   builder: (data, documentId) {
//   //     return data ?? {};
//   //   },
//   // );
//   List<Map> response = await APIService.apiRequest('/organizations');
//     print('RESPONSE:');
//     print(response);
//     return response.map((org) => Organization.fromMap(org)).toList();
// });
