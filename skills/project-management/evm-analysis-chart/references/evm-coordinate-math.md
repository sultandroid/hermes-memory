# EVM S-Curve Coordinate Math

## Y-axis formula

```
y = chartBottom - (value_in_K / scaleFactor)
```

Where:
- `chartBottom` = Y-coordinate of the 0-value line on the chart
- `value_in_K` = the value in thousands of SAR (e.g., 614 for 614K)
- `scaleFactor` = pixels per 1K SAR (typically 4)

Example: For a chart with bottom at y=379 and scale=4:
- 614K → y = 379 - 614/4 = 379 - 153.5 = 225
- 538K → y = 379 - 538/4 = 379 - 134.5 = 244
- 467K → y = 379 - 467/4 = 379 - 116.75 = 262

## Polyline data points

EV S-curve should use monthly cumulative data points:
```
Feb=20K(374), Mar=50K(366), Apr=120K(349), May=300K(304), Jun=538K(244)
```

PV uses planned values:
```
Feb=30K(371), Mar=90K(356), Apr=200K(329), May=400K(279), Jun=614K(225)
```

AC uses actual payments:
```
Feb=10K(376), Mar=30K(371), Apr=135K(345), May=345K(293), Jun=467K(262)
```

## SVG chart dimensions

Standard: width=650, height=1000 (viewport)
Chart area: x=0, y=130, width=650, height=370
X-axis months spaced ~90px apart starting at x=100

## Arrow calculations

SV arrow: from EV y-coord to PV y-coord at today's x-position
CV arrow: from AC y-coord to EV y-coord at today's x-position
- If EV > AC → CV is positive (green arrow, EV above AC)
- If AC > EV → CV is negative (red arrow, AC above EV)
