// Cannlytics Data
// Copyright (c) 2023 Cannlytics

// Authors:
//   Keegan Skeate <https://github.com/keeganskeate>
// Created: 5/7/2023
// Updated: 5/7/2023
// License: MIT License <https://github.com/cannlytics/cannlytics/blob/main/LICENSE>
// Original code: <https://gist.github.com/pskink/afd4f20a40ae7756555877ec030daa46>
// Map Credit: MapSVG <https://mapsvg.com/maps>
// Map License: CC-BY 4.0 <https://creativecommons.org/licenses/by/4.0/>
import 'dart:math';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:path_drawing/path_drawing.dart';
import 'package:xml/xml.dart';
import 'package:go_router/go_router.dart';

// Global map properties.
const String mapSvg = 'assets/images/maps/usa-with-labels.svg';
final Color mapBorderColor = Colors.grey.shade400;
const Duration mapAnimationDuration = Duration(milliseconds: 400);

/// An interactive map of the united states.
class InteractiveMap extends StatefulWidget {
  @override
  State<InteractiveMap> createState() => _InteractiveMapState();
}

/// Map state.
class _InteractiveMapState extends State<InteractiveMap>
    with TickerProviderStateMixin {
  // Properties.
  MapData? mapData;
  late Animation<Matrix4> animation;
  late ExtendedViewport extendedViewport;

  // Controllers.
  late final animationController =
      AnimationController(vsync: this, duration: mapAnimationDuration);
  TransformationController? transformationController;

  // Initialization.
  @override
  void initState() {
    super.initState();
    animationController
        .addListener(() => transformationController?.value = animation.value);
    _parseSvg().then((value) {
      setState(() => mapData = value);
    });
  }

  /// Dispose controllers.
  @override
  void dispose() {
    super.dispose();
    animationController.dispose();
    transformationController?.dispose();
  }

  /// Scale a rectangle.
  Matrix4 rectToRect(
    Rect src,
    Rect dst, {
    BoxFit fit = BoxFit.contain,
    Alignment alignment = Alignment.center,
  }) {
    FittedSizes fs = applyBoxFit(fit, src.size, dst.size);
    double scaleX = fs.destination.width / fs.source.width;
    double scaleY = fs.destination.height / fs.source.height;
    Size fittedSrc = Size(src.width * scaleX, src.height * scaleY);
    Rect out = alignment.inscribe(fittedSrc, dst);
    return Matrix4.identity()
      ..translate(out.left, out.top)
      ..scale(scaleX, scaleY)
      ..translate(-src.left, -src.top);
  }

  /// Zoom to a rectangle.
  Matrix4 _zoomTo(String id, Size size) {
    return rectToRect(
      mapData!.states[id]!.rect,
      Offset.zero & size,
      fit: BoxFit.contain,
    );
  }

  /// Initialize controller.
  TransformationController _initController(Size size) {
    final matrix = rectToRect(
      Offset.zero & mapData!.size,
      Offset.zero & size,
      fit: BoxFit.contain,
    );
    final ctrl = TransformationController(matrix);
    extendedViewport = ExtendedViewport(
      ctrl: ctrl,
      cacheFactor: 1.75,
    );

    // Initial zoom.
    Future.delayed(const Duration(milliseconds: 0), () {
      animation = Matrix4Tween(
        begin: ctrl.value,
        end: _zoomTo('labels', size),
      ).animate(animationController);
      animationController
        ..value = 0
        ..animateTo(
          1,
          curve: Curves.easeInExpo,
          duration: const Duration(milliseconds: 0),
        );
    });
    return ctrl;
  }

  /// Render the widget.
  @override
  Widget build(BuildContext context) {
    // Loading indicator.
    if (mapData == null) {
      return const Center(child: CircularProgressIndicator(strokeWidth: 1.42));
    }

    // Render the map.
    return Theme(
      data: Theme.of(context).copyWith(splashFactory: _InkFactory()),
      child: LayoutBuilder(builder: (context, constraints) {
        transformationController ??= _initController(constraints.biggest);
        extendedViewport.size = constraints.biggest;
        return ColoredBox(
          color: Theme.of(context).cardColor,
          child: InteractiveViewer(
            constrained: true,
            transformationController: transformationController,
            maxScale: 10,
            child: Flow(
              delegate: MapDelegate(mapData!, extendedViewport),
              children: mapData!.states.values
                  .map((stateData) =>
                      _shapeBuilder(stateData, constraints.biggest))
                  .toList(),
            ),
          ),
        );
      }),
    );
  }

  /// Render shape.
  Widget _shapeBuilder(StateData stateData, Size size) {
    final shape = StateBorder(stateData.path.shift(-stateData.rect.topLeft));
    return DecoratedBox(
      decoration: ShapeDecoration(
        shape: shape,

        /// FIXME: Color appropriately.
        // gradient: stateData.gradient,
        // shadows: const [
        //   BoxShadow(blurRadius: 0.5),
        //   BoxShadow(blurRadius: 0.5, offset: Offset(0.5, 0.5)),
        // ],
      ),
      child: Material(
        type: MaterialType.transparency,
        clipBehavior: Clip.antiAlias,
        shape: shape,
        child: InkWell(
          // Highlight.
          highlightColor: Colors.transparent,

          // Action.
          onTap: () {
            if (stateData.id == 'labels') {
              // FIXME:
              return;
            }
            context.push('/licenses/${stateData.id.toLowerCase()}');
          },

          // Optional: Label.
          // child: Center(
          //     child: Text(
          //   stateData.id,
          //   textScaleFactor: 0.1,
          // )),
        ),
      ),
    );
  }

  /// Parse the map SVG.
  Future<MapData> _parseSvg() async {
    // Read the SVG.
    final xml = await rootBundle.loadString(mapSvg);
    final doc = XmlDocument.parse(xml);

    // Get the dimensions.
    final w = double.parse(doc.rootElement.getAttribute('width')!);
    final h = double.parse(doc.rootElement.getAttribute('height')!);

    // Determine colors.
    // FIXME: Color by cannabis status.
    List<Color> colors(double h) {
      return [
        HSVColor.fromAHSV(1, h * 360, 1, 0.9).toColor(),
        HSVColor.fromAHSV(1, h * 360, 1, 0.3).toColor(),
      ];
    }

    const padding = EdgeInsets.all(40);
    final allCountries = doc.rootElement.findElements('path');
    final numCountries = allCountries.length;
    final states = allCountries.mapIndexed((i, stateData) => StateData(
          path: parseSvgPathData(stateData.getAttribute('d')!)
              .shift(padding.topLeft),
          id: stateData.getAttribute('id') ?? 'id_$i ???',
          title: stateData.getAttribute('title') ?? 'title_$i ???',
          // FIXME: Assign color by status.
          gradient: LinearGradient(
            colors: colors(i / numCountries),
            stops: const [0.2, 1],
          ),
          seqNo: i,
        ));
    return MapData(
      size: Size(w + padding.horizontal, h + padding.vertical),
      states: {
        for (final stateData in states) stateData.id: stateData,
      },
    );
  }
}

/// Map delegate.
class MapDelegate extends FlowDelegate {
  MapDelegate(this.mapData, this.extendedViewport)
      : super(repaint: extendedViewport);

  // Properties.
  final MapData mapData;
  final ValueNotifier<Rect> extendedViewport;

  /// Paint the children.
  @override
  void paintChildren(FlowPaintingContext context) {
    final filteredCountries = mapData.states.values
        .where((stateData) => stateData.rect.overlaps(extendedViewport.value));
    for (final stateData in filteredCountries) {
      final offset = stateData.rect.topLeft;
      context.paintChild(stateData.seqNo,
          transform: Matrix4.translationValues(offset.dx, offset.dy, 0));
    }
    // print('paintChildren, ${filteredCountries.map((c) => c.id)}');
  }

  /// Get the constraints for a shape.
  @override
  BoxConstraints getConstraintsForChild(int i, BoxConstraints constraints) {
    // print('getConstraintsForChild $i');
    final stateData = mapData.states.values.elementAt(i);
    return BoxConstraints.tight(stateData.rect.size);
  }

  /// Get the size of the map.
  @override
  Size getSize(BoxConstraints constraints) => mapData.size;

  /// Determine if a repaint is needed.
  @override
  bool shouldRepaint(covariant FlowDelegate oldDelegate) => false;
}

/// Map model.
class MapData {
  MapData({
    required this.size,
    required this.states,
  });

  final Size size;
  final Map<String, StateData> states;
}

/// Map state model.
class StateData {
  StateData({
    required this.path,
    required this.id,
    required this.title,
    required this.gradient,
    required this.seqNo,
  }) : rect = path.getBounds();

  final Path path;
  final Rect rect;
  final String id;
  final String title;
  final Gradient gradient;
  final int seqNo;
}

/// Map viewport.
class ExtendedViewport extends ValueNotifier<Rect> {
  ExtendedViewport({
    required this.ctrl,
    required this.cacheFactor,
  }) : super(Rect.largest) {
    ctrl.addListener(_buildViewport);
  }

  // Set the size of the map.
  final TransformationController ctrl;
  final double cacheFactor;
  Size _size = Size.zero;
  set size(Size size) {
    if (size != _size) {
      _size = size;
    }
  }

  Rect innerRect = Rect.zero;
  double prevScale = 0;

  // Build the viewport.
  _buildViewport() {
    assert(_size != Size.zero);
    final offset = ctrl.toScene(_size.center(Offset.zero));
    final scale = ctrl.value.getMaxScaleOnAxis();

    if (!innerRect.contains(offset) || scale != prevScale) {
      prevScale = scale;
      value = Rect.fromCenter(
        center: offset,
        width: _size.width * cacheFactor / scale,
        height: _size.height * cacheFactor / scale,
      );
      // print('value: $value');
      innerRect = EdgeInsets.symmetric(
        horizontal: _size.width * 0.5 / scale,
        vertical: _size.height * 0.5 / scale,
      ).deflateRect(value);
    }
  }
}

/// State border.
class StateBorder extends ShapeBorder {
  const StateBorder(this.path);

  // Properties.
  final Path path;

  // Dimensions.
  @override
  EdgeInsetsGeometry get dimensions => EdgeInsets.zero;

  // Get the inner path.
  @override
  Path getInnerPath(Rect rect, {TextDirection? textDirection}) =>
      getOuterPath(rect);

  // Get the outer path.
  @override
  Path getOuterPath(Rect rect, {TextDirection? textDirection}) {
    return rect.topLeft == Offset.zero ? path : path.shift(rect.topLeft);
  }

  // Render the border.
  @override
  void paint(Canvas canvas, Rect rect, {TextDirection? textDirection}) {
    canvas
      ..save()
      ..clipPath(path)
      ..drawPath(
          path,
          Paint()
            ..style = PaintingStyle.stroke
            ..strokeWidth = 0.25
            ..color = Colors.grey.shade400)
      ..restore();
  }

  @override
  ShapeBorder scale(double t) => this;
}

class _InkFactory extends InteractiveInkFeatureFactory {
  @override
  InteractiveInkFeature create({
    required MaterialInkController controller,
    required RenderBox referenceBox,
    required Offset position,
    required Color color,
    required TextDirection textDirection,
    bool containedInkWell = false,
    RectCallback? rectCallback,
    BorderRadius? borderRadius,
    ShapeBorder? customBorder,
    double? radius,
    VoidCallback? onRemoved,
  }) {
    return _InkFeature(
      controller: controller,
      referenceBox: referenceBox,
      color: color,
      position: position,
    );
  }
}

class _InkFeature extends InteractiveInkFeature {
  _InkFeature({
    required MaterialInkController controller,
    required RenderBox referenceBox,
    required Color color,
    required this.position,
  }) : super(controller: controller, referenceBox: referenceBox, color: color) {
    _controller = AnimationController(
        duration: mapAnimationDuration, vsync: controller.vsync)
      ..addListener(controller.markNeedsPaint)
      ..forward();
    controller.addInkFeature(this);
  }

  static const gradient = LinearGradient(
    colors: [Colors.amber, Colors.deepOrange],
  );

  late AnimationController _controller;
  final Offset position;

  @override
  void confirm() => _controller.reverse().then((value) => dispose());

  @override
  void cancel() => _controller.reverse().then((value) => dispose());

  @override
  void dispose() {
    super.dispose();
    _controller.dispose();
  }

  @override
  void paintFeature(Canvas canvas, Matrix4 transform) {
    final scale = referenceBox.getTransformTo(null).getMaxScaleOnAxis();
    final t = Curves.easeInOut.transform(_controller.value);
    final rect = Offset.zero & referenceBox.size;
    final side = 2 * rect.bottomRight.distance;

    // FIXME: Color the states appropriately.
    // lerpDouble(100, 255, _controller.value)!.toInt(), 0, 0, 0)
    final paint = Paint()
      ..color = Color.fromARGB(33, 0, 0, 0)
      ..shader = gradient.createShader(rect);
    final matrix = composeMatrixFromOffsets(
      anchor: position,
      translate: position,
      rotation: pi * .75 * t,
    );
    final hFactor = const Cubic(1, 0, 1, 1).transform(t);
    final path = Path()
      ..addOval(
        Rect.fromCenter(
            center: position,
            width: side * _controller.value,
            height: (48 / scale + side * hFactor) * _controller.value),
      );
    canvas
      ..save()
      ..transform(matrix.storage)
      ..drawPath(path, paint)
      ..restore();
  }
}

/// Compose a matrix from offsets.
Matrix4 composeMatrixFromOffsets({
  double scale = 1,
  double rotation = 0,
  Offset translate = Offset.zero,
  Offset anchor = Offset.zero,
}) {
  final double c = cos(rotation) * scale;
  final double s = sin(rotation) * scale;
  final double dx = translate.dx - c * anchor.dx + s * anchor.dy;
  final double dy = translate.dy - s * anchor.dx - c * anchor.dy;
  return Matrix4(c, s, 0, 0, -s, c, 0, 0, 0, 0, 1, 0, dx, dy, 0, 1);
}
