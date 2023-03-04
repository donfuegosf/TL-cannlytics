// Cannlytics App
// Copyright (c) 2023 Cannlytics
// Copyright (c) 2021 Coding With Flutter Limited

// Authors:
//   Keegan Skeate <https://github.com/keeganskeate>
// Created: 2/17/2023
// Updated: 2/23/2023
// License: MIT License <https://github.com/cannlytics/cannlytics/blob/main/LICENSE>
// License: MIT License <https://github.com/bizz84/code_with_andrea_flutter/blob/main/LICENSE.md>

// Flutter imports:
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

// Package imports:
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_web_plugins/url_strategy.dart';
import 'package:shared_preferences/shared_preferences.dart';

// Project imports:
import 'package:cannlytics_app/constants/colors.dart';
import 'package:cannlytics_app/firebase_options.dart';
import 'package:cannlytics_app/routing/app_router.dart';
import 'package:cannlytics_app/services/auth_service.dart';
import 'package:cannlytics_app/services/theme_service.dart';
import 'package:cannlytics_app/ui/account/onboarding/onboarding_controller.dart';
import 'package:cannlytics_app/utils/strings/string_hardcoded.dart';

// ignore: depend_on_referenced_packages

// ignore:depend_on_referenced_packages

/// The main application.
class CannlyticsApp extends ConsumerWidget {
  const CannlyticsApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Routing provider.
    final goRouter = ref.watch(goRouterProvider);

    // Theme provider.
    final themeMode = ref.watch(themeModeProvider);

    // Remove the native splash screen.
    // FlutterNativeSplash.remove();

    // Material app.
    return MaterialApp.router(
      debugShowCheckedModeBanner: false,
      routerConfig: goRouter,
      theme: AppColors.toThemeData(false),
      darkTheme: AppColors.toThemeData(true),
      themeMode: themeMode,
    );
  }
}

/// [main] initializes the [CannlyticsApp].
Future<void> main() async {
  // Initialize Flutter.
  WidgetsBinding widgetsBinding = WidgetsFlutterBinding.ensureInitialized();

  // Keep the native splash screen open until the app initializes.
  // FlutterNativeSplash.preserve(widgetsBinding: widgetsBinding);

  // Initialize Firebase.
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);

  // Remove hashtags from URLs on the web.
  usePathUrlStrategy();

  // Register error handlers.
  final sharedPreferences = await SharedPreferences.getInstance();
  registerErrorHandlers();

  // TODO: Register licenses.
  LicenseRegistry.addLicense(() async* {
    // final license = await rootBundle.loadString('google_fonts/OFL.txt');
    // yield LicenseEntryWithLineBreaks(['google_fonts'], license);
  });

  // Create a container to serve as the app entry point.
  final container = ProviderContainer(
    overrides: [
      onboardingStoreProvider
          .overrideWithValue(OnboardingStore(sharedPreferences)),
    ],
  );

  // Wait for authentication to be determined.
  // Note: This will prevent unnecessary redirects when the app starts.
  await container.read(userProvider.future);
  runApp(UncontrolledProviderScope(
    container: container,
    child: const CannlyticsApp(),
  ));
}

/// [registerErrorHandlers] displays notifications if certain errors are thrown.
void registerErrorHandlers() {
  // Show an error notification if any uncaught exception happens.
  FlutterError.onError = (FlutterErrorDetails details) {
    FlutterError.presentError(details);
    debugPrint(details.toString());
  };

  // Handle underlying platform/OS errors.
  PlatformDispatcher.instance.onError = (Object error, StackTrace stack) {
    debugPrint(error.toString());
    return true;
  };

  // Show an error notification when any widget in the app fails to build.
  ErrorWidget.builder = (FlutterErrorDetails details) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.red,
        title: Text('An error occurred'.hardcoded),
      ),
      body: Center(child: Text(details.toString())),
    );
  };
}
