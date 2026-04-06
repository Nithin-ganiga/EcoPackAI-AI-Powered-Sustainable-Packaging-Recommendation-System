"""This file handles PDF and Excel report generation for packaging recommendations using reportlab and openpyxl libraries."""

import io
from datetime import datetime
from typing import List

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.colors import HexColor

import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from schemas import ReportRequest


# Color constants
GREEN = HexColor("#27AE60")
DARK_GREEN = HexColor("#1E8449")
LIGHT_GREEN = HexColor("#D5F5E3")
NAVY = HexColor("#1A1A2E")
WHITE = colors.white
GRAY = HexColor("#7F8C8D")
LIGHT_GRAY = HexColor("#F8F9FA")

TIER_COLORS = {
    "Excellent": HexColor("#27AE60"),
    "Good": HexColor("#2980B9"),
    "Average": HexColor("#F39C12"),
    "Poor": HexColor("#E74C3C"),
}


def generate_pdf_report(report_data: ReportRequest) -> bytes:
    """Generate complete PDF recommendation report and return as bytes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()
    custom_styles = {
        "header_title": ParagraphStyle(
            "header_title",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=WHITE,
            alignment=TA_CENTER,
            spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "report_title": ParagraphStyle(
            "report_title",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=GREEN,
            alignment=TA_CENTER,
            spaceAfter=10,
            fontName="Helvetica-Bold",
        ),
        "section_heading": ParagraphStyle(
            "section_heading",
            parent=styles["Heading2"],
            fontSize=12,
            textColor=GREEN,
            spaceAfter=8,
            spaceBefore=8,
            fontName="Helvetica-Bold",
        ),
        "normal_text": ParagraphStyle(
            "normal_text",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.black,
            alignment=TA_LEFT,
        ),
        "normal_center": ParagraphStyle(
            "normal_center",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.black,
            alignment=TA_CENTER,
        ),
        "small_text": ParagraphStyle(
            "small_text",
            parent=styles["Normal"],
            fontSize=8,
            textColor=colors.black,
        ),
        "italic_text": ParagraphStyle(
            "italic_text",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.black,
            fontName="Helvetica-Oblique",
        ),
        "label_bold": ParagraphStyle(
            "label_bold",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.black,
            fontName="Helvetica-Bold",
        ),
    }

    story = []

    # Header Section - Navy background
    header_table_data = [
        [Paragraph("<b>EcoPackAI</b>", custom_styles["header_title"])],
    ]
    header_table = Table(header_table_data, colWidths=[19 * cm])
    header_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), NAVY),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ])
    )
    story.append(header_table)
    story.append(Spacer(1, 0.2 * cm))

    # Report title
    story.append(Paragraph("Packaging Material Recommendation Report", custom_styles["report_title"]))
    story.append(HRFlowable(width="100%", thickness=2, color=GREEN))
    story.append(Spacer(1, 0.4 * cm))

    # Search Details Section
    story.append(Paragraph("Search Details", custom_styles["section_heading"]))
    search_details_data = [
        [
            Paragraph("<b>Product Name</b>", custom_styles["label_bold"]),
            Paragraph(str(report_data.product_name), custom_styles["normal_text"]),
        ],
        [
            Paragraph("<b>Product Weight</b>", custom_styles["label_bold"]),
            Paragraph(f"{report_data.product_weight_grams:.2f} grams", custom_styles["normal_text"]),
        ],
        [
            Paragraph("<b>Fragility Level</b>", custom_styles["label_bold"]),
            Paragraph(str(report_data.fragility).capitalize(), custom_styles["normal_text"]),
        ],
    ]
    search_table = Table(search_details_data, colWidths=[5 * cm, 10 * cm])
    search_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (1, -1), LIGHT_GRAY),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ])
    )
    story.append(search_table)
    story.append(Spacer(1, 0.2 * cm))

    # Generated timestamp
    generated_date = datetime.fromisoformat(report_data.generated_at).strftime("%B %d, %Y at %H:%M:%S")
    story.append(Paragraph(f"<i>Generated on {generated_date}</i>", custom_styles["italic_text"]))
    story.append(HRFlowable(width="100%", thickness=1, color=GREEN))
    story.append(Spacer(1, 0.4 * cm))

    # Best Pick Section
    if report_data.recommendations:
        best_material = report_data.recommendations[0]
        story.append(Paragraph("👑 Best Recommendation", custom_styles["section_heading"]))
        best_pick_data = [
            [
                Paragraph(f"<b>{best_material.material_name}</b>", ParagraphStyle(
                    "best_name",
                    parent=custom_styles["normal_text"],
                    fontSize=11,
                    fontName="Helvetica-Bold",
                    textColor=GREEN,
                )),
                Paragraph(f"<b>{best_material.sustainability_tier}</b>", ParagraphStyle(
                    "best_tier",
                    parent=custom_styles["normal_center"],
                    fontSize=10,
                    fontName="Helvetica-Bold",
                    textColor=WHITE,
                    backColor=TIER_COLORS.get(best_material.sustainability_tier, GRAY),
                )),
            ],
        ]
        best_pick_table = Table(best_pick_data, colWidths=[12 * cm, 7 * cm])
        best_pick_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREEN),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("BORDER", (0, 0), (-1, -1), 1, GREEN),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LIGHT_GREEN]),
            ])
        )
        story.append(best_pick_table)

        # Best pick stats
        best_stats = [
            [
                Paragraph(f"<b>Cost:</b><br/>${best_material.cost_inr:.2f} INR", custom_styles["small_text"]),
                Paragraph(f"<b>Strength:</b><br/>{best_material.strength}", custom_styles["small_text"]),
                Paragraph(f"<b>Score:</b><br/>{best_material.suitability_score:.1f}/10", custom_styles["small_text"]),
                Paragraph(f"<b>CO2:</b><br/>{best_material.co2_emission_score}", custom_styles["small_text"]),
            ],
        ]
        best_stats_table = Table(best_stats, colWidths=[4.75 * cm, 4.75 * cm, 4.75 * cm, 4.75 * cm])
        best_stats_table.setStyle(
            TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
            ])
        )
        story.append(best_stats_table)
        story.append(Spacer(1, 0.2 * cm))

        # Why recommended
        story.append(Paragraph(f"<i>{best_material.why_recommended}</i>", custom_styles["italic_text"]))
        story.append(HRFlowable(width="100%", thickness=1, color=GREEN))
        story.append(Spacer(1, 0.4 * cm))

    # Top 5 Recommendations Table
    story.append(Paragraph("All 5 Recommendations", custom_styles["section_heading"]))

    table_headers = [
        "Rank",
        "Material",
        "Type",
        "Strength",
        "Cost (₹)",
        "Eco",
        "Fragility",
        "Score",
        "Tier",
    ]
    table_data = [table_headers]

    for rec in report_data.recommendations:
        table_data.append([
            str(rec.rank),
            rec.material_name,
            rec.material_type,
            rec.strength,
            f"₹{rec.cost_inr:.0f}",
            "Yes" if rec.eco_friendly else "No",
            rec.fragility_support,
            f"{rec.suitability_score:.1f}",
            rec.sustainability_tier,
        ])

    colwidths = [0.8 * cm, 2.5 * cm, 1.8 * cm, 1.5 * cm, 1.3 * cm, 1 * cm, 1.5 * cm, 1.2 * cm, 1.5 * cm]
    recommendations_table = Table(table_data, colWidths=colwidths)

    table_style_list = [
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTSIZE", (0, 1), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, HexColor("#F0FAF4")]),
        ("BACKGROUND", (0, 1), (-1, 1), HexColor("#D5F5E3")),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
    ]

    # Color tier cells
    for row in range(1, len(table_data)):
        tier_value = table_data[row][8]
        tier_color = TIER_COLORS.get(tier_value, GRAY)
        table_style_list.append(("BACKGROUND", (8, row), (8, row), tier_color))
        table_style_list.append(("TEXTCOLOR", (8, row), (8, row), WHITE))
        table_style_list.append(("FONTNAME", (8, row), (8, row), "Helvetica-Bold"))

    recommendations_table.setStyle(TableStyle(table_style_list))
    story.append(recommendations_table)
    story.append(Spacer(1, 0.4 * cm))

    # Detailed Material Cards
    story.append(Paragraph("Detailed Material Profiles", custom_styles["section_heading"]))

    for material in report_data.recommendations:
        # Card header
        card_header = [
            [
                Paragraph(f"<b>Rank {material.rank}</b>", custom_styles["label_bold"]),
                Paragraph(f"<b>{material.material_name}</b>", ParagraphStyle(
                    "card_name",
                    parent=custom_styles["normal_text"],
                    fontSize=10,
                    fontName="Helvetica-Bold",
                )),
                Paragraph(f"<b>{material.sustainability_tier}</b>", ParagraphStyle(
                    "card_tier",
                    parent=custom_styles["normal_center"],
                    textColor=WHITE,
                    backColor=TIER_COLORS.get(material.sustainability_tier, GRAY),
                    fontSize=9,
                    fontName="Helvetica-Bold",
                )),
            ],
        ]
        card_header_table = Table(card_header, colWidths=[1.5 * cm, 11 * cm, 6.5 * cm])
        card_header_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ])
        )
        story.append(card_header_table)

        # Card details
        card_details = [
            [
                Paragraph(f"<b>Material Type:</b>", custom_styles["label_bold"]),
                Paragraph(material.material_type, custom_styles["normal_text"]),
                Paragraph(f"<b>Cost (INR):</b>", custom_styles["label_bold"]),
                Paragraph(f"₹{material.cost_inr:.2f}", custom_styles["normal_text"]),
            ],
            [
                Paragraph(f"<b>Industry:</b>", custom_styles["label_bold"]),
                Paragraph(material.industry, custom_styles["normal_text"]),
                Paragraph(f"<b>Cost Level:</b>", custom_styles["label_bold"]),
                Paragraph(material.cost_level, custom_styles["normal_text"]),
            ],
            [
                Paragraph(f"<b>Strength:</b>", custom_styles["label_bold"]),
                Paragraph(material.strength, custom_styles["normal_text"]),
                Paragraph(f"<b>Eco Friendly:</b>", custom_styles["label_bold"]),
                Paragraph("Yes" if material.eco_friendly else "No", custom_styles["normal_text"]),
            ],
            [
                Paragraph(f"<b>Weight Capacity:</b>", custom_styles["label_bold"]),
                Paragraph(material.weight_capacity, custom_styles["normal_text"]),
                Paragraph(f"<b>Fragility Support:</b>", custom_styles["label_bold"]),
                Paragraph(material.fragility_support, custom_styles["normal_text"]),
            ],
            [
                Paragraph(f"<b>Suitability Score:</b>", custom_styles["label_bold"]),
                Paragraph(f"{material.suitability_score:.2f}/10", custom_styles["normal_text"]),
                Paragraph(f"<b>CO2 Score:</b>", custom_styles["label_bold"]),
                Paragraph(str(material.co2_emission_score), custom_styles["normal_text"]),
            ],
            [
                Paragraph(f"<b>Biodegradability:</b>", custom_styles["label_bold"]),
                Paragraph(f"{material.biodegradability_score}%", custom_styles["normal_text"]),
                Paragraph(f"<b>Recyclability:</b>", custom_styles["label_bold"]),
                Paragraph(f"{material.recyclability_percent}%", custom_styles["normal_text"]),
            ],
        ]

        card_details_table = Table(card_details, colWidths=[3.5 * cm, 5.5 * cm, 3.5 * cm, 5.5 * cm])
        card_details_table.setStyle(
            TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, HexColor("#F8F9FA")]),
            ])
        )
        story.append(card_details_table)

        # Why recommended
        why_rec = [
            [
                Paragraph(f"<b>Why Recommended:</b>", custom_styles["label_bold"]),
                Paragraph(f"<i>{material.why_recommended}</i>", custom_styles["italic_text"]),
            ],
        ]
        why_table = Table(why_rec, colWidths=[3.5 * cm, 15.5 * cm])
        why_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREEN),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, GREEN),
            ])
        )
        story.append(why_table)
        story.append(Spacer(1, 0.3 * cm))

    # Footer
    story.append(HRFlowable(width="100%", thickness=1, color=GRAY))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "<i>Report generated by EcoPackAI - AI-Powered Packaging Recommendation System</i>",
        ParagraphStyle(
            "footer",
            parent=custom_styles["small_text"],
            fontSize=7,
            textColor=GRAY,
            alignment=TA_CENTER,
        ),
    ))
    story.append(Paragraph(
        "<i>Disclaimer: This report is generated based on ML model predictions and rule-based analysis.</i>",
        ParagraphStyle(
            "disclaimer",
            parent=custom_styles["small_text"],
            fontSize=7,
            textColor=GRAY,
            alignment=TA_CENTER,
        ),
    ))

    doc.build(story)
    return buffer.getvalue()


def generate_excel_report(report_data: ReportRequest) -> bytes:
    """Generate complete Excel recommendation report and return as bytes."""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # Sheet 1: Search Summary
    ws_summary = wb.create_sheet("Search Summary", 0)
    _create_summary_sheet(ws_summary, report_data)

    # Sheet 2: Top 5 Recommendations
    ws_recommendations = wb.create_sheet("Recommendations", 1)
    _create_recommendations_sheet(ws_recommendations, report_data)

    # Sheet 3: Material Details
    ws_details = wb.create_sheet("Material Details", 2)
    _create_details_sheet(ws_details, report_data)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()


def _create_summary_sheet(ws, report_data: ReportRequest):
    """Create the Summary sheet with search details and best recommendation."""
    header_fill = PatternFill(patternType="solid", fgColor="27AE60")
    header_font = Font(name="Calibri", bold=True, color="FFFFFF", size=14)
    label_font = Font(name="Calibri", bold=True, color="2C3E50", size=11)
    normal_font = Font(name="Calibri", color="000000", size=11)
    border = Border(
        left=Side(style="thin", color="95A5A6"),
        right=Side(style="thin", color="95A5A6"),
        top=Side(style="thin", color="95A5A6"),
        bottom=Side(style="thin", color="95A5A6"),
    )

    # Title
    ws.merge_cells("A1:F1")
    title_cell = ws["A1"]
    title_cell.value = "EcoPackAI - Packaging Recommendation Report"
    title_cell.fill = PatternFill(patternType="solid", fgColor="1A1A2E")
    title_cell.font = Font(name="Calibri", bold=True, color="FFFFFF", size=16)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30

    ws.row_dimensions[2].height = 5

    # Search Details Section
    ws.merge_cells("A3:F3")
    search_header = ws["A3"]
    search_header.value = "SEARCH DETAILS"
    search_header.fill = header_fill
    search_header.font = header_font
    search_header.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[3].height = 22

    # Search details rows
    details = [
        ("Product Name", report_data.product_name),
        ("Product Weight", f"{report_data.product_weight_grams:.2f} grams"),
        ("Fragility Level", report_data.fragility.capitalize()),
        ("Generated At", report_data.generated_at),
    ]

    row = 4
    for label, value in details:
        ws[f"A{row}"].value = label
        ws[f"A{row}"].font = label_font
        ws[f"A{row}"].fill = PatternFill(patternType="solid", fgColor="ECF0F1")
        ws[f"A{row}"].border = border

        ws.merge_cells(f"B{row}:F{row}")
        ws[f"B{row}"].value = value
        ws[f"B{row}"].font = normal_font
        ws[f"B{row}"].border = border
        ws.row_dimensions[row].height = 18
        row += 1

    row += 1

    # Best Recommendation Section
    if report_data.recommendations:
        best = report_data.recommendations[0]

        ws.merge_cells(f"A{row}:F{row}")
        best_header = ws[f"A{row}"]
        best_header.value = "BEST RECOMMENDATION"
        best_header.fill = header_fill
        best_header.font = header_font
        best_header.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[row].height = 22
        row += 1

        best_details = [
            ("Material Name", best.material_name),
            ("Sustainability Tier", best.sustainability_tier),
            ("Predicted Cost (INR)", f"₹{best.cost_inr:.2f}"),
            ("Suitability Score", f"{best.suitability_score:.2f}/10"),
            ("Eco Friendly", "Yes" if best.eco_friendly else "No"),
            ("Fragility Support", best.fragility_support),
            ("Why Recommended", best.why_recommended),
        ]

        for label, value in best_details:
            ws[f"A{row}"].value = label
            ws[f"A{row}"].font = label_font
            ws[f"A{row}"].fill = PatternFill(patternType="solid", fgColor="ECF0F1")
            ws[f"A{row}"].border = border

            ws.merge_cells(f"B{row}:F{row}")
            ws[f"B{row}"].value = value
            ws[f"B{row}"].font = normal_font
            ws[f"B{row}"].border = border
            ws[f"B{row}"].alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[row].height = 18
            row += 1

    ws.column_dimensions["A"].width = 25
    ws.column_dimensions["B"].width = 45
    ws.column_dimensions["C"].width = 15
    ws.column_dimensions["D"].width = 15
    ws.column_dimensions["E"].width = 15
    ws.column_dimensions["F"].width = 15


def _create_recommendations_sheet(ws, report_data: ReportRequest):
    """Create the Recommendations sheet with all 5 materials in table format."""
    header_fill = PatternFill(patternType="solid", fgColor="27AE60")
    header_font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
    border = Border(
        left=Side(style="thin", color="95A5A6"),
        right=Side(style="thin", color="95A5A6"),
        top=Side(style="thin", color="95A5A6"),
        bottom=Side(style="thin", color="95A5A6"),
    )

    # Title
    ws.merge_cells("A1:O1")
    title_cell = ws["A1"]
    title_cell.value = "EcoPackAI - Top 5 Packaging Recommendations"
    title_cell.fill = PatternFill(patternType="solid", fgColor="1A1A2E")
    title_cell.font = Font(name="Calibri", bold=True, color="FFFFFF", size=14)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 25

    # Product info
    ws.merge_cells("A2:O2")
    info_cell = ws["A2"]
    info_cell.value = f"Product: {report_data.product_name} | Weight: {report_data.product_weight_grams:.2f}g | Fragility: {report_data.fragility.capitalize()}"
    info_cell.font = Font(name="Calibri", size=10, italic=True)
    info_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 18

    ws.row_dimensions[3].height = 5

    # Headers
    headers = [
        "Rank",
        "Material Name",
        "Material Type",
        "Industry",
        "Strength",
        "Weight Capacity",
        "Cost (₹)",
        "Cost Level",
        "Eco Friendly",
        "Fragility Support",
        "Suitability Score",
        "CO2 Score",
        "Biodegradability",
        "Recyclability",
        "Tier",
    ]

    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=4, column=col)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
    ws.row_dimensions[4].height = 25

    # Data rows
    tier_colors_map = {
        "Excellent": "27AE60",
        "Good": "2980B9",
        "Average": "F39C12",
        "Poor": "E74C3C",
    }

    for row_idx, rec in enumerate(report_data.recommendations, start=5):
        bg_color = "A9DFBF" if row_idx == 5 else ("FFFFFF" if row_idx % 2 == 0 else "F0FAF4")

        data = [
            rec.rank,
            rec.material_name,
            rec.material_type,
            rec.industry,
            rec.strength,
            rec.weight_capacity,
            f"{rec.cost_inr:.0f}",
            rec.cost_level,
            "Yes" if rec.eco_friendly else "No",
            rec.fragility_support,
            f"{rec.suitability_score:.2f}",
            rec.co2_emission_score,
            f"{rec.biodegradability_score}%",
            f"{rec.recyclability_percent}%",
            rec.sustainability_tier,
        ]

        for col, value in enumerate(data, start=1):
            cell = ws.cell(row=row_idx, column=col)
            cell.value = value
            cell.fill = PatternFill(patternType="solid", fgColor=bg_color)
            cell.border = border
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.font = Font(name="Calibri", size=10)

            # Color tier cells
            if col == 15:
                tier_color = tier_colors_map.get(value, "95A5A6")
                cell.fill = PatternFill(patternType="solid", fgColor=tier_color)
                cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")

            # Color eco friendly
            if col == 9:
                if value == "Yes":
                    cell.font = Font(name="Calibri", size=10, bold=True, color="27AE60")
                else:
                    cell.font = Font(name="Calibri", size=10, bold=True, color="E74C3C")

        ws.row_dimensions[row_idx].height = 18

    # Column widths
    column_widths = {
        "A": 6,
        "B": 20,
        "C": 16,
        "D": 16,
        "E": 12,
        "F": 16,
        "G": 10,
        "H": 12,
        "I": 12,
        "J": 16,
        "K": 16,
        "L": 10,
        "M": 16,
        "N": 12,
        "O": 12,
    }

    for col_letter, width in column_widths.items():
        ws.column_dimensions[col_letter].width = width

    # Freeze panes
    ws.freeze_panes = "A5"


def _create_details_sheet(ws, report_data: ReportRequest):
    """Create the Material Details sheet with detailed info for each material."""
    header_fill = PatternFill(patternType="solid", fgColor="27AE60")
    header_font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
    label_font = Font(name="Calibri", bold=True, color="2C3E50", size=10)
    normal_font = Font(name="Calibri", size=10)
    border = Border(
        left=Side(style="thin", color="95A5A6"),
        right=Side(style="thin", color="95A5A6"),
        top=Side(style="thin", color="95A5A6"),
        bottom=Side(style="thin", color="95A5A6"),
    )

    ws.merge_cells("A1:B1")
    title_cell = ws["A1"]
    title_cell.value = "EcoPackAI - Detailed Material Profiles"
    title_cell.fill = PatternFill(patternType="solid", fgColor="1A1A2E")
    title_cell.font = Font(name="Calibri", bold=True, color="FFFFFF", size=14)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 25

    row = 2

    tier_colors_map = {
        "Excellent": "27AE60",
        "Good": "2980B9",
        "Average": "F39C12",
        "Poor": "E74C3C",
    }

    for material in report_data.recommendations:
        # Material header
        ws.merge_cells(f"A{row}:B{row}")
        header_cell = ws[f"A{row}"]
        header_cell.value = f"Rank {material.rank} - {material.material_name}"
        header_cell.fill = header_fill
        header_cell.font = header_font
        header_cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[row].height = 20
        row += 1

        # Details
        details_data = [
            ("Material Type", material.material_type),
            ("Industry", material.industry),
            ("Strength", material.strength),
            ("Weight Capacity", material.weight_capacity),
            ("Cost (INR)", f"₹{material.cost_inr:.2f}"),
            ("Cost Level", material.cost_level),
            ("Eco Friendly", "Yes" if material.eco_friendly else "No"),
            ("Fragility Support", material.fragility_support),
            ("Suitability Score", f"{material.suitability_score:.2f}/10"),
            ("CO2 Emission Score", material.co2_emission_score),
            ("Biodegradability Score", f"{material.biodegradability_score}%"),
            ("Recyclability Percent", f"{material.recyclability_percent}%"),
            ("Sustainability Tier", material.sustainability_tier),
        ]

        for label, value in details_data:
            ws[f"A{row}"].value = label
            ws[f"A{row}"].font = label_font
            ws[f"A{row}"].fill = PatternFill(patternType="solid", fgColor="ECF0F1")
            ws[f"A{row}"].border = border
            ws[f"A{row}"].alignment = Alignment(horizontal="left", vertical="center")

            ws[f"B{row}"].value = value
            ws[f"B{row}"].font = normal_font
            ws[f"B{row}"].border = border
            ws[f"B{row}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

            # Color tier value
            if label == "Sustainability Tier":
                ws[f"B{row}"].fill = PatternFill(patternType="solid", fgColor=tier_colors_map.get(value, "95A5A6"))
                ws[f"B{row}"].font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")

            # Color eco friendly value
            if label == "Eco Friendly":
                if value == "Yes":
                    ws[f"B{row}"].font = Font(name="Calibri", size=10, bold=True, color="27AE60")
                else:
                    ws[f"B{row}"].font = Font(name="Calibri", size=10, bold=True, color="E74C3C")

            ws.row_dimensions[row].height = 18
            row += 1

        # Why recommended
        ws[f"A{row}"].value = "Why Recommended"
        ws[f"A{row}"].font = label_font
        ws[f"A{row}"].fill = PatternFill(patternType="solid", fgColor="D5F5E3")
        ws[f"A{row}"].border = border
        ws[f"A{row}"].alignment = Alignment(horizontal="left", vertical="top")

        ws[f"B{row}"].value = material.why_recommended
        ws[f"B{row}"].font = Font(name="Calibri", size=10, italic=True)
        ws[f"B{row}"].fill = PatternFill(patternType="solid", fgColor="D5F5E3")
        ws[f"B{row}"].border = border
        ws[f"B{row}"].alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

        ws.row_dimensions[row].height = 25
        row += 2

    ws.column_dimensions["A"].width = 25
    ws.column_dimensions["B"].width = 50
