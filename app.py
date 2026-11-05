import json
import requests
import streamlit as st

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyq6eeltu92qxTflIt-BWamPw2ev2FzZOj5j7qiMrj3lHYyyBNArf1zmLF0g2PDuS3-Jg/exec"

DEFAULT_ASIA_COUNTRIES = [
    "Vietnam",
    "Indonesia",
    "Thailand",
    "Malaysia",
    "Philippines",
    "Singapore",
    "India",
    "Taiwan",
    "Myanmar",
    "Cambodia",
    "Laos",
    "Pakistan",
    "Brunei",
]

st.set_page_config(
    page_title="Asia Regional Channel Intelligence 2027",
    page_icon="🌏",
    layout="wide",
)

st.title("🌏 Asia Regional Channel Intelligence & Growth Plan 2027 / 2027年亚洲区域渠道情报与增长计划")
st.markdown(
    "Welcome! Please use this friendly portal to submit your country channel "
    "assessments, competitor insights, and 2027 growth initiatives. Data flows "
    "directly into our master Google Sheet automatically.\n\n"
    "欢迎使用！请通过此友好门户提交您的国家渠道评估、竞争对手洞察以及 2027 年增长计划。数据将自动直接流向我们的主 Google 表格。"
)

st.sidebar.header("⚙️ Admin Panel / 管理面板")
st.sidebar.subheader("Manage Asia Countries / 管理亚洲国家")
country_input = st.sidebar.text_area(
    "Country List / 国家列表:", "\n".join(DEFAULT_ASIA_COUNTRIES)
)
countries = [c.strip() for c in country_input.split("\n") if c.strip()]

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📋 Instructions & Metadata / 指南与元数据",
        "📊 Country Assessment (Sheet 1) / 国家渠道评估 (表1)",
        "🏢 Competitor Analysis (Sheet 2) / 竞争对手分析 (表2)",
        "🚀 Growth & Investment Plan (Sheet 3) / 增长与投资计划 (表3)",
        "📖 Admin & User Manual / 管理员与用户手册",
    ]
)

with tab1:
    st.header("Project Timeline & Submission Details / 项目时间表与提交详情")
    st.info(
        "**Target Submission Date / 目标提交日期:** 30th Nov 2026 | **Consolidation Body / 汇总机构:** Asia "
        "Regional Marketing & Channel Strategy Team / 亚洲区域营销与渠道战略团队"
    )
    col1, col2 = st.columns(2)
    with col1:
        selected_country = st.selectbox("Select Your Country / Region / 选择您的国家/地区", countries)
        submitter_name = st.text_input(
            "Completed By / Title / 填写人 / 职位", placeholder="e.g., John Doe / Country Manager (例如: John Doe / 国家经理)"
        )
    with col2:
        submission_date = st.date_input("Submission Date / 提交日期")
        regional_reviewer = st.text_input(
            "Regional Reviewer / 区域审核人", placeholder="e.g., Regional Strategy Director (例如: 区域战略总监)"
        )

with tab2:
    st.header("Sheet 1: Country Channel Assessment (PCR & TBR Segmented) / 表1：国家渠道评估（PCR 和 TBR 分割）")
    col_pcr, col_tbr = st.columns(2)
    with col_pcr:
        st.subheader("🚗 PCR Segment (Passenger Car Radial) / PCR乘用车胎细分市场")
        pcr_model = st.selectbox(
            "PCR Main Channel Model / PCR主要渠道模式",
            [
                "Sole Distributor / 独家经销商",
                "Regional Distributor / 区域经销商", 
                "Wholesale Direct / 批发直销",
                "Dealer / 经销商", 
                "SCS Retail Flagship / SCS零售旗舰店",
                "Multi-Brand Retail / 多品牌零售",
                "KA / 重点客户",
            ],
            key="pcr_m",
        )
        pcr_partners = st.text_input(
            "PCR Key Channel Partners / PCR主要渠道合作伙伴",
            "Key PCR Distributors & Master Dealers / 核心PCR经销商与总代理",
            key="pcr_p",
        )
        pcr_margin = st.slider("PCR Average Channel Margin (%) / PCR平均渠道毛利率 (%)", 5, 35, 15, key="pcr_mg")
        pcr_rating = st.selectbox(
            "PCR Logistics & Delivery Rating / PCR物流与交付评级",
            ["Strong / 强", "Medium / 中", "Weak / 弱"],
            key="pcr_r",
        )
    with col_tbr:
        st.subheader("🚛 TBR Segment (Truck & Bus Radial) / TBR卡客车胎细分市场")
        tbr_model = st.selectbox(
            "TBR Main Channel Model / TBR主要渠道模式",
            [
                "Sole Distributor / 独家经销商",
                "Regional Distributor / 区域经销商", 
                "Dealer / 经销商",
                "STS Retail Flagship / STS零售旗舰店",
                "KA / 重点客户",
            ],
            key="tbr_m",
        )
        tbr_partners = st.text_input(
            "TBR Key Channel Partners / TBR主要渠道合作伙伴",
            "Key TBR Fleet Distributors & Dealers / 核心TBR车队经销商与代理商",
            key="tbr_p",
        )
        tbr_margin = st.slider("TBR Average Channel Margin (%) / TBR平均渠道毛利率 (%)", 5, 35, 12, key="tbr_mg")
        tbr_rating = st.selectbox(
            "TBR Logistics & Delivery Rating / TBR物流与交付评级",
            ["Strong / 强", "Medium / 中", "Weak / 弱"],
            key="tbr_r",
        )

    if st.button("💾 Save Country Assessment to Google Sheets / 保存国家评估至Google表格", type="primary"):
        payload = {
            "tabName": "Country Channel Assessment",
            "rowValues": [
                str(submission_date),
                selected_country,
                submitter_name,
                pcr_model,
                pcr_partners,
                pcr_margin,
                pcr_rating,
                tbr_model,
                tbr_partners,
                tbr_margin,
                tbr_rating,
            ],
        }
        try:
            res = requests.post(GOOGLE_SCRIPT_URL, json=payload)
            if res.status_code == 200:
                st.success("✅ Successfully saved to Google Sheets! / 成功保存至Google表格！")
            else:
                st.error("❌ Failed to reach endpoint. / 无法连接到端点。")
        except Exception as e:
            st.error(f"Error / 错误: {e}")

with tab3:
    st.header("Sheet 2: Top 3 Competitors Analysis / 表2：前三大竞争对手分析")
    with st.form("competitor_form"):
        comp_brand = st.text_input(
            "Competitor Brand Name / 竞争对手品牌名称",
            placeholder="e.g., Bridgestone, Michelin, GT Radial (例如：普利司通、米其林、佳通)",
        )
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            comp_segment = st.selectbox(
                "Product Segment / 产品细分市场", ["PCR", "TBR", "Both / 两者", "Joint / 联合"]
            )
            comp_tier = st.text_input(
                "Brand Positioning & Price Tier / 品牌定位与价格层级",
                "Tier 1 Premium (100% Price Index) / 一线高端 (100%价格指数)",
            )
            comp_threat = st.selectbox("Threat Level / 威胁级别", ["High / 高", "Medium / 中", "Low / 低"])
        with col_c2:
            comp_adv = st.text_area(
                "Distribution Advantage / 分销优势", "Dominant OEM fitments and dealer ties / 主导配套和经销商纽带"
            )
            comp_weak = st.text_input(
                "Main Weakness / 主要劣势", "High price point in budget fleets / 经济型车队中价格点偏高"
            )
        comp_strategy = st.text_area(
            "Recommended Counter-Strategy / 建议应对策略",
            "Target fleet cost-per-km efficiency with TBR programs / 利用TBR项目针对车队每公里成本效益",
        )
        if st.form_submit_button("🚀 Submit Competitor Analysis / 提交竞争对手分析", type="primary"):
            payload = {
                "tabName": "Top 3 Competitors",
                "rowValues": [
                    selected_country,
                    comp_brand,
                    comp_segment,
                    comp_tier,
                    comp_adv,
                    comp_weak,
                    comp_threat,
                    comp_strategy,
                ],
            }
            requests.post(GOOGLE_SCRIPT_URL, json=payload)
            st.success("✅ Competitor recorded! / 竞争对手记录成功！")

with tab4:
    st.header("Sheet 3: 2027 Growth & Investment Plan (New Initiative Builder) / 表3：2027年增长与投资计划（新举措构建器）")
    with st.form("initiative_form"):
        init_title = st.text_input(
            "Strategic Initiative / Action Title / 战略举措 / 行动标题",
            "Retail Shopfront Signboard & POSM Upgrade / 零售店面招牌及物料升级",
        )
        col_i1, col_i2, col_i3 = st.columns(3)
        with col_i1:
            init_segment = st.selectbox(
                "Product Segment / 产品细分市场", ["PCR", "TBR", "Both / 两者", "Joint / 联合"], key="init_seg"
            )
            baseline_vol = st.number_input(
                "2026 Baseline Volume (pcs) / 2026年基准销量 (条)", value=20000, step=500
            )
        with col_i2:
            region_chan = st.text_input("Region / Channel / 区域 / 渠道", "North Region / 北部区域")
            target_vol = st.number_input(
                "2027 Target Volume (pcs) / 2027年目标销量 (条)", value=35000, step=500
            )
        with col_i3:
            investment_usd = st.number_input(
                "Estimated Investment (USD) / 预计投资额 (美元)", value=15000, step=1000
            )
            cost_cat = st.selectbox(
                "Cost Category / 成本类别",
                [
                    "Channel Development / 渠道发展",
                    "Marketing Support / 营销支持",
                    "Commercial Support / 商务支持",
                ],
            )

        col_i4, col_i5, col_i6 = st.columns(3)
        with col_i4:
            owner = st.text_input("Responsible Owner / 负责人", "Sales - PCR Lead / 销售-PCR负责人")
            priority = st.selectbox("Priority Level / 优先级", ["High / 高", "Medium / 中", "Low / 低"])
        with col_i5:
            target_date = st.date_input("Target Completion Date / 目标完成日期")
            status = st.selectbox(
                "Status / 状态", ["Planned / 已计划", "In Progress / 进行中", "Under Review / 审核中", "Completed / 已完成"]
            )
        with col_i6:
            roi = st.text_input("Expected ROI / Payback / 预期投资回报 / 回本期", "18 Months / 18个月")
            support_req = st.text_input(
                "Regional Support Required / 所需区域支持", "POSM Design & Co-op Budget / 物料设计与合作预算"
            )

        talent_req = st.text_input(
            "Talent & Capability Requirement / 人才与能力需求",
            "Retail visual merchandising & training / 零售视觉陈列与培训",
        )
        digital_tool = st.text_input(
            "Digital Enablement Tool / Platform / 数字赋能工具 / 平台", "Digital Signage Asset Portal / 数字标牌资产门户"
        )
        risk_mitigation = st.text_input(
            "Channel Conflict Mitigation Risk / 渠道冲突缓解风险",
            "Standardized co-op guidelines / 标准化合作指南",
        )

        if st.form_submit_button(
            "🚀 Submit New Strategic Initiative / 提交新战略举措", type="primary"
        ):
            vol_growth = target_vol - baseline_vol
            payload = {
                "tabName": "2027 Growth & Investment Plan",
                "rowValues": [
                    selected_country,
                    init_title,
                    init_segment,
                    region_chan,
                    baseline_vol,
                    target_vol,
                    vol_growth,
                    investment_usd,
                    cost_cat,
                    roi,
                    owner,
                    str(target_date),
                    priority,
                    support_req,
                    status,
                    talent_req,
                    digital_tool,
                    risk_mitigation,
                ],
            }
            requests.post(GOOGLE_SCRIPT_URL, json=payload)
            st.success("✅ New Strategic Initiative saved! / 新战略举措已保存！")

with tab5:
    st.header("📖 Manual Book for Admins & Users / 管理员与用户手册")
    st.markdown("""
        ### 👋 Welcome to the Asia Channel Intelligence Portal! / 欢迎来到亚洲渠道情报门户！
        This web app was built to collect regional data seamlessly into your Google Sheet.\n
        本网页应用旨在无缝收集各区域数据并直接存入您的 Google 表格。
        """)
