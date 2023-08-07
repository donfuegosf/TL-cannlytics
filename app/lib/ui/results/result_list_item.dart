// Cannlytics Data
// Copyright (c) 2023 Cannlytics

// Authors:
//   Keegan Skeate <https://github.com/keeganskeate>
// Created: 5/23/2023
// Updated: 8/6/2023
// License: MIT License <https://github.com/cannlytics/cannlytics/blob/main/LICENSE>

// Flutter imports:
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

// Package imports:
import 'package:url_launcher/url_launcher.dart';

// Project imports:
import 'package:cannlytics_data/constants/colors.dart';
import 'package:cannlytics_data/constants/design.dart';
import 'package:cannlytics_data/models/lab_result.dart';
import 'package:cannlytics_data/services/download_service.dart';

/// A lab result list item.
/// Optional: Add image.
class LabResultItem extends StatelessWidget {
  LabResultItem({required this.labResult});

  // Properties
  final LabResult labResult;

  @override
  Widget build(BuildContext context) {
    // Style and theme.
    final screenWidth = MediaQuery.of(context).size.width;
    bool isDark = Theme.of(context).brightness == Brightness.dark;

    print('Building list item:');
    print(labResult.toMap());
    return Card(
      margin: EdgeInsets.symmetric(horizontal: 24),
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(3)),
      color: Theme.of(context).scaffoldBackgroundColor,
      surfaceTintColor: Theme.of(context).scaffoldBackgroundColor,
      child: Container(
        margin: EdgeInsets.all(0),
        padding: EdgeInsets.all(16.0),
        decoration: BoxDecoration(borderRadius: BorderRadius.circular(3.0)),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            // Product name and COA link.
            Row(
              children: [
                if (screenWidth <= Breakpoints.tablet)
                  Expanded(
                    child: Text(
                      labResult.productName ?? 'Unknown',
                      style: Theme.of(context).textTheme.labelLarge,
                    ),
                  ),
                if (screenWidth > Breakpoints.tablet)
                  Text(
                    labResult.productName ?? 'Unknown',
                    style: Theme.of(context).textTheme.labelLarge,
                  ),

                // Download COA data.
                GestureDetector(
                  onTap: () {
                    // Handle malformed results.
                    var data = labResult.toMap();
                    if (data['results'] == null) {
                      data['results'] = [];
                    }

                    // Show a downloading notification.
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text(
                          'Preparing your download...',
                          style: Theme.of(context).textTheme.bodyMedium,
                        ),
                        duration: Duration(seconds: 2),
                        backgroundColor:
                            isDark ? DarkColors.green : LightColors.lightGreen,
                        showCloseIcon: true,
                      ),
                    );

                    // Download the data.
                    DownloadService.downloadData(
                      [data],
                      '/api/data/coas/download',
                    );
                  },
                  child: Icon(
                    Icons.download_sharp,
                    color: Theme.of(context).textTheme.labelMedium!.color,
                    size: 16,
                  ),
                ),

                // Open COA URL link.
                if (labResult.downloadUrl?.isNotEmpty ?? false) gapW8,
                if (labResult.downloadUrl?.isNotEmpty ?? false)
                  GestureDetector(
                    onTap: () {
                      launchUrl(Uri.parse(labResult.downloadUrl!));
                    },
                    child: Icon(
                      Icons.open_in_new,
                      color: Theme.of(context).textTheme.labelMedium!.color,
                      size: 16,
                    ),
                  ),
              ],
            ),
            gapH8,

            // Producer.
            // Future work: Link to producer website.
            Text(
              'Producer: ${labResult.businessDbaName != null && labResult.businessDbaName!.isNotEmpty ? labResult.businessDbaName : labResult.producer}',
              style: Theme.of(context).textTheme.labelMedium,
            ),

            // IDs
            Text(
              'ID: ${labResult.labId}',
              style: Theme.of(context).textTheme.labelMedium,
            ),
            Text(
              'Batch: ${labResult.batchNumber}',
              style: Theme.of(context).textTheme.labelMedium,
            ),

            // Lab.
            Row(
              children: [
                Text(
                  'Lab: ',
                  style: Theme.of(context).textTheme.labelMedium,
                ),
                GestureDetector(
                  onTap: () {
                    launchUrl(Uri.parse(labResult.labWebsite!));
                  },
                  child: Text(
                    labResult.lab!,
                    style: Theme.of(context).textTheme.labelMedium!.copyWith(
                          color: Colors.blue,
                        ),
                  ),
                ),
              ],
            ),

            // Copy COA link.
            if (labResult.downloadUrl?.isNotEmpty ?? false) gapH4,
            if (labResult.downloadUrl?.isNotEmpty ?? false)
              _coaLink(context, labResult.downloadUrl!),
          ],
        ),
      ),
    );
  }

  /// Copy COA link.
  Widget _coaLink(BuildContext context, String url) {
    // Theme.
    bool isDark = Theme.of(context).brightness == Brightness.dark;

    return InkWell(
      onTap: () async {
        await Clipboard.setData(ClipboardData(text: url));
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Copied link!',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            duration: Duration(seconds: 2),
            backgroundColor: isDark ? DarkColors.green : LightColors.lightGreen,
            showCloseIcon: true,
          ),
        );
      },
      child: Padding(
        padding: EdgeInsets.symmetric(vertical: 8, horizontal: 12),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            Icon(Icons.link, size: 12, color: Colors.blueAccent),
            SizedBox(width: 4),
            Text(
              'Copy COA link',
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.bold,
                color: Colors.blueAccent,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
