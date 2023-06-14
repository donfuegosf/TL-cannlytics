// Cannlytics Data
// Copyright (c) 2023 Cannlytics

// Authors:
//   Keegan Skeate <https://github.com/keeganskeate>
// Created: 5/7/2023
// Updated: 5/16/2023
// License: MIT License <https://github.com/cannlytics/cannlytics/blob/main/LICENSE>

// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:dartx/dartx.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_typeahead/flutter_typeahead.dart';
import 'package:go_router/go_router.dart';

// Project imports:
import 'package:cannlytics_data/common/buttons/secondary_button.dart';
import 'package:cannlytics_data/common/dialogs/auth_dialogs.dart';
import 'package:cannlytics_data/common/forms/form_placeholder.dart';
import 'package:cannlytics_data/ui/layout/breadcrumbs.dart';
import 'package:cannlytics_data/ui/layout/console.dart';
import 'package:cannlytics_data/ui/layout/footer.dart';
import 'package:cannlytics_data/ui/layout/header.dart';
import 'package:cannlytics_data/ui/layout/sidebar.dart';
import 'package:cannlytics_data/common/tables/table_data.dart';
import 'package:cannlytics_data/constants/design.dart';
import 'package:cannlytics_data/services/auth_service.dart';
import 'package:cannlytics_data/services/data_service.dart';
import 'package:cannlytics_data/services/storage_service.dart';
import 'package:cannlytics_data/ui/licensees/licensees_controller.dart';
import 'package:cannlytics_data/utils/utils.dart';

/// Screen.
class StateLicensesScreen extends StatelessWidget {
  const StateLicensesScreen({super.key, required this.id});

  // Properties.
  final String id;

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    return Scaffold(
      // App bar.
      appBar: DashboardHeader(),

      // Side menu.
      drawer: Responsive.isMobile(context) ? MobileDrawer() : null,

      // Body.
      body: Console(slivers: [
        // Breadcrumbs.
        SliverToBoxAdapter(
          child: Padding(
            padding: EdgeInsets.only(
              left: sliverHorizontalPadding(screenWidth) / 2,
              right: sliverHorizontalPadding(screenWidth) / 2,
              top: 24,
            ),
            child: _breadcrumbs(context),
          ),
        ),

        // Table.
        SliverToBoxAdapter(
          child: SingleChildScrollView(
            child: Padding(
              padding: EdgeInsets.only(
                left: sliverHorizontalPadding(screenWidth) / 2,
                right: sliverHorizontalPadding(screenWidth) / 2,
                top: 24,
              ),
              child: Column(children: [LicenseesTable(id: id)]),
            ),
          ),
        ),

        // Footer.
        const SliverToBoxAdapter(child: Footer()),
      ]),
    );
  }

  /// Page breadcrumbs.
  Widget _breadcrumbs(BuildContext context) {
    return Row(
      children: [
        Breadcrumbs(
          items: [
            BreadcrumbItem(
                title: 'Data',
                onTap: () {
                  context.push('/');
                }),
            BreadcrumbItem(
                title: 'Licenses',
                onTap: () {
                  context.push('/licenses');
                }),
            BreadcrumbItem(
              title: id.toUpperCase(),
            ),
          ],
        ),
      ],
    );
  }
}

/// Table.
class LicenseesTable extends ConsumerWidget {
  const LicenseesTable({super.key, required this.id});
  final String id;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Listen to the filtered licensees.
    final data = ref.watch(filteredLicenseesProvider).value!;

    // FIXME:: Loading data placeholder.
    // return asyncData.when(
    //   data: (obj) => _form(context, obj),
    //   loading: () => _loadingIndicator(),
    //   error: (error, stack) => _errorMessage(context, error, stack),
    // );

    // No data placeholder.
    if (data.isEmpty) {
      return FormPlaceholder(
        image: 'assets/images/icons/document.png',
        title: 'No licenses found',
        description:
            'Either there are no active licenses in this state or the data has not yet been populated.\nPlease contact dev@cannlytics.com to get a person on this ASAP.',
        onTap: () {
          context.push('/licenses');
        },
      );
    }

    // Listen to the current user.
    final user = ref.watch(authProvider).currentUser;

    // Responsive screen width.
    // final screenWidth = MediaQuery.of(context).size.width;

    // Define the cell builder function.
    _buildCells(Map item) {
      var values = [
        item['license_number'],
        item['business_legal_name'],
        item['license_type'],
        item['premise_city'],
      ];
      return values.map((value) {
        return DataCell(
          Text(value),
          onTap: () {
            // FIXME: This doesn't update the URL correctly.
            String slug = WebUtils.slugify(item['id']);
            context.go('/licenses/$id/$slug');
          },
        );
      }).toList();
    }

    // Define the table headers.
    List<Map> headers = [
      {'name': 'License number', 'key': 'license_number', 'sort': true},
      {
        'name': 'Business legal name',
        'key': 'business_legal_name',
        'sort': true
      },
      {'name': 'License type', 'key': 'license_type', 'sort': true},
      {'name': 'Premise city', 'key': 'premise_city', 'sort': false},
    ];

    // Format the table headers.
    List<DataColumn> tableHeader = <DataColumn>[
      for (Map header in headers)
        DataColumn(
          label: Expanded(
            child: Text(
              header['name'],
              style: TextStyle(fontStyle: FontStyle.italic),
            ),
          ),
          onSort: (columnIndex, sortAscending) {
            var field = headers[columnIndex]['key'];
            var sort = headers[columnIndex]['sort'];
            if (!sort) return;
            // ignore: unused_local_variable
            var sorted = data;
            if (sortAscending) {
              sorted = data.sortedBy((x) => x.toMap()[field]);
            } else {
              sorted = data.sortedByDescending((x) => x.toMap()[field]);
            }
            ref.read(licenseesSortColumnIndex.notifier).state = columnIndex;
            ref.read(licenseesSortAscending.notifier).state = sortAscending;
            // FIXME:
            // ref.read(licenseesProvider.notifier).setLicensees(sorted);
          },
        ),
    ];

    // Get the rows per page.
    final rowsPerPage = ref.watch(licenseesRowsPerPageProvider);

    // Get the sorting state.
    final sortColumnIndex = ref.read(licenseesSortColumnIndex);
    final sortAscending = ref.read(licenseesSortAscending);

    // Build the data table.
    Widget table = PaginatedDataTable(
      // Options.
      showCheckboxColumn: false,
      showFirstLastButtons: true,
      sortColumnIndex: sortColumnIndex,
      sortAscending: sortAscending,

      // Columns
      columns: tableHeader,

      // Style.
      dataRowHeight: 48,
      columnSpacing: 48,
      headingRowHeight: 48,
      horizontalMargin: 0,

      // Pagination.
      availableRowsPerPage: [5, 10, 25, 50, 100],
      rowsPerPage: rowsPerPage,
      onRowsPerPageChanged: (index) {
        ref.read(licenseesRowsPerPageProvider.notifier).state = index!;
      },

      // Table.
      source: TableData<Map<String, dynamic>>(
        data: data,
        cellsBuilder: _buildCells,
      ),
    );

    // Read the search controller.
    final _controller = ref.watch(licenseesSearchController);

    // Define the table actions.
    var actions = Row(
      children: [
        // Search box.
        SizedBox(
          width: 175,
          child: TypeAheadField(
            textFieldConfiguration: TextFieldConfiguration(
              // Controller.
              controller: _controller,

              // Decoration.
              decoration: InputDecoration(
                hintText: 'Search...',
                contentPadding:
                    EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.all(Radius.circular(3)),
                ),
                suffixIcon: _controller.text.isNotEmpty
                    ? GestureDetector(
                        onTap: () {
                          ref.read(searchTermProvider.notifier).state = '';
                          _controller.clear();
                        },
                        child: Icon(Icons.clear),
                      )
                    : null,
              ),
              style: DefaultTextStyle.of(context)
                  .style
                  .copyWith(fontStyle: FontStyle.italic),
            ),

            // Search engine function.
            suggestionsCallback: (pattern) async {
              ref.read(searchTermProvider.notifier).state = pattern;
              final suggestions = ref.read(filteredLicenseesProvider);
              return suggestions.value!;
            },

            // Autocomplete menu.
            itemBuilder:
                (BuildContext context, Map<String, dynamic>? suggestion) {
              return ListTile(title: Text(suggestion!['business_legal_name']));
            },

            // Menu selection function.
            onSuggestionSelected: (Map<String, dynamic>? suggestion) {
              // FIXME: What to do?
              // context.push('/licenses/$id/${suggestion!['id']}');
            },
          ),
        ),

        // Download button.
        Spacer(),
        SecondaryButton(
          text: 'Download',
          onPressed: () async {
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

            // Get download URL from Firebase Storage.
            String storageRef = 'data/licenses/$id/licenses-$id-latest.csv';
            String? url = await StorageService.getDownloadUrl(storageRef);
            if (url == null) return;

            // Download the datafile.
            DataService.openInANewTab(url);
          },
        ),
      ],
    );

    // No data placeholder.
    if (data.isEmpty)
      table = FormPlaceholder(
        image: 'assets/images/icons/document.png',
        title: 'No licenses found',
        description:
            'Either there are no active licenses in this state or the data has not yet been populated.\nPlease contact dev@cannlytics.com to get a person on this ASAP.',
        onTap: () {
          context.push('/licenses');
        },
      );

    // Return the widget.
    table = Material(
      // color: Theme.of(context).secondaryHeaderColor,
      color: Colors.transparent,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(3.0)),
      child: table,
    );
    return Column(children: [actions, gapH12, table]);
  }
}

/// Data rows.
// class DataSource extends DataTableSource {
//   DataSource(this.list);

//   // Properties.
//   final List<Map<String, dynamic>> list;

//   int _selectedCount = 0;

//   @override
//   int get rowCount => list.length;

//   @override
//   bool get isRowCountApproximate => false;

//   @override
//   int get selectedRowCount => _selectedCount;

//   @override
//   DataRow getRow(int index) {
//     return DataRow.byIndex(
//       index: index,
//       cells: _buildCells(list[index]),
//       color: MaterialStateColor.resolveWith(_getDataRowColor),
//     );
//   }

//   // Define the color of the row.
//   Color _getDataRowColor(Set<MaterialState> states) {
//     const Set<MaterialState> interactiveStates = <MaterialState>{
//       MaterialState.pressed,
//       MaterialState.hovered,
//       MaterialState.focused,
//     };
//     if (states.any(interactiveStates.contains)) {
//       return Colors.grey;
//     }
//     return Colors.transparent;
//   }

//   // Define the cell builder function.
//   _buildCells(Map item) {
//     var values = [
//       item['license_number'],
//       item['business_legal_name'],
//       item['license_type'],
//       item['premise_city'],
//     ];
//     return values.map((value) {
//       return DataCell(
//         Text(value),
//         onTap: () {
//           String slug = WebUtils.slugify(item['id']);
//           print('NAVIGATE TO SLUG: $slug');
//           // context.push('/licenses/$id/$slug');
//         },
//       );
//     }).toList();
//   }
// }
