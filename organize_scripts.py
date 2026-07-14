import os
import shutil

base_dir = r"d:\AI-Cyborg-2558\_SEO_Clients\RWC"
scripts_dir = os.path.join(base_dir, "scripts")

categories = {
    "google_sheets": [
        "add_combined_summary.py", "add_compare_columns.py", "add_eng_rate_col.py", 
        "analyze_sheet.py", "check_formulas.py", "check_rows.py", "check_sheet_headers.py", 
        "check_target.py", "check_zero_time.py", "delete_l_m_n.py", "fix_all_columns.py", 
        "fix_col_l_o.py", "fix_col_n_all_rows.py", "fix_headers_newline.py", "fix_ytd_data.py", 
        "inspect_sheets.py", "print_hij.py", "print_urls.py", "read_worksheet.py", 
        "refactor_col_l_header_and_format.py", "remove_column_h.py", "revert_col_o.py", 
        "split_yoy_columns.py", "update_col_i_active_users.py", "update_l_and_p.py", 
        "update_service_types.py", "update_sheet_types.py", "verify_col_l.py"
    ],
    "ga4": [
        "fetch_ga4_all_rows.py", "fetch_ga4_yoy.py", "fix_ga4_built_comparisons.py", 
        "fix_ga4_compare_dates.py", "fix_ga4_double_encode.py", "fix_ga4_exact_template.py", 
        "fix_ga4_links.py", "fix_ga4_seldim.py", "fix_triple_encode.py", "query_ga4_verify.py", 
        "query_page_duration.py", "restore_compare_links.py", "test_ga4_access.py", 
        "test_ga4_admin.py", "test_ga4_organic.py", "test_ga4_row4.py", "test_ga4_row4_past.py"
    ],
    "wordpress": [
        "check_filler_count.py", "count_types.py", "extract_filler_urls.py", 
        "find_missing_articles.py", "update_redirect_status.py"
    ],
    "gsc": [
        "check_gsc_access.py"
    ],
    "reports": [
        "generate_filler_report.py"
    ]
}

# Create base scripts dir
if not os.path.exists(scripts_dir):
    os.makedirs(scripts_dir)

# Create categories and move files
for category, files in categories.items():
    cat_dir = os.path.join(scripts_dir, category)
    if not os.path.exists(cat_dir):
        os.makedirs(cat_dir)
        
    for f in files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(cat_dir, f)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"Moved {f} to {category}/")
        else:
            print(f"File not found: {f}")

print("Organization complete!")
