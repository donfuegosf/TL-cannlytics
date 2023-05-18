// Cannlytics Data
// Copyright (c) 2023 Cannlytics

// Authors:
//   Keegan Skeate <https://github.com/keeganskeate>
// Created: 4/15/2023
// Updated: 5/12/2023
// License: MIT License <https://github.com/cannlytics/cannlytics/blob/main/LICENSE>

// TODO: Links to places where users can get their COAs:
// ACS Labs: https://portal.acslabcannabis.com/clientpage
// Curaleaf: https://curaleaf.com/transparency
// Fluent: https://getfluent.com/testresults/
// Jungle Boys: https://www.jungleboys.com/verify/
// Sunnyside: https://www.verifyhemp.com/
// Trulieve: https://www.trulieve.com/discover/product-test-search

// Flutter imports:
import 'package:cannlytics_data/common/cards/card_grid.dart';
import 'package:cannlytics_data/common/cards/stats_model_card.dart';
import 'package:cannlytics_data/common/dialogs/auth_dialogs.dart';
import 'package:cannlytics_data/services/auth_service.dart';
import 'package:cannlytics_data/services/data_service.dart';
import 'package:cannlytics_data/services/storage_service.dart';
import 'package:cannlytics_data/ui/dashboard/dashboard_controller.dart';
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

// Project imports:
import 'package:cannlytics_data/common/layout/breadcrumbs.dart';
import 'package:cannlytics_data/common/layout/console.dart';
import 'package:cannlytics_data/common/layout/footer.dart';
import 'package:cannlytics_data/common/layout/header.dart';
import 'package:cannlytics_data/common/layout/sidebar.dart';
import 'package:cannlytics_data/constants/design.dart';
import 'package:intl/intl.dart';
import 'coa_doc_ui.dart';

/// Screen.
class LabResultsScreen extends StatelessWidget {
  const LabResultsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // App bar.
      appBar: DashboardHeader(),

      // Side menu.
      drawer: Responsive.isMobile(context) ? MobileDrawer() : null,

      // Body.
      body: Console(slivers: [
        // Main content.
        SliverToBoxAdapter(child: MainContent()),

        // Footer.
        const SliverToBoxAdapter(child: Footer()),
      ]),
    );
  }
}

/// Main content.
class MainContent extends ConsumerWidget {
  const MainContent({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Dynamic screen width.
    final screenWidth = MediaQuery.of(context).size.width;

    // Render the widget.
    return Padding(
      padding: EdgeInsets.only(
        left: sliverHorizontalPadding(screenWidth),
        right: sliverHorizontalPadding(screenWidth),
        top: 24,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          // Breadcrumbs.
          Row(
            children: [
              Breadcrumbs(
                items: [
                  BreadcrumbItem(
                      title: 'Data',
                      onTap: () {
                        context.go('/');
                      }),
                  BreadcrumbItem(
                    title: 'Lab Results',
                  )
                ],
              ),
            ],
          ),

          // Your Results
          gapH12,
          CoADocInterface(),

          // Lab results datasets.
          gapH32,
          _datasetsCards(context, ref),
          gapH48,
        ],
      ),
    );
  }

  /// Dataset cards.
  Widget _datasetsCards(BuildContext context, WidgetRef ref) {
    var datasets =
        mainDatasets.where((element) => element['type'] == 'results').toList();
    final screenWidth = MediaQuery.of(context).size.width;
    final user = ref.watch(authProvider).currentUser;
    return Column(children: [
      Row(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          Text('Lab Results Datasets',
              style: Theme.of(context).textTheme.labelLarge!.copyWith(
                  color: Theme.of(context).textTheme.titleLarge!.color)),
        ],
      ),
      gapH12,
      CardGridView(
        crossAxisCount: screenWidth < Breakpoints.desktop ? 1 : 2,
        childAspectRatio: 3,
        items: datasets.map((model) {
          return DatasetCard(
            imageUrl: model['image_url'],
            title: model['title'],
            description: model['description'],
            tier: model['tier'],
            rows: NumberFormat('#,###').format(model['observations']) + ' rows',
            columns: NumberFormat('#,###').format(model['fields']) + ' columns',
            onTap: () async {
              // Note: Requires the user to be signed in.
              if (user == null) {
                showDialog(
                  context: context,
                  builder: (BuildContext context) {
                    return SignInDialog(isSignUp: false);
                  },
                );
                return;
              }
              // Get URL for file in Firebase Storage.
              String? url =
                  await StorageService.getDownloadUrl(model['file_ref']);
              DataService.openInANewTab(url);
            },
          );
        }).toList(),
      ),
    ]);
  }
}
