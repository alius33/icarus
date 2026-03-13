"""Generate a branded PDF of the CLARA-Gainsight Integration Charter."""
from fpdf import FPDF
import textwrap

# Moody's brand
NAVY = (9, 17, 100)     # #091164
BLUE = (0, 94, 255)     # #005eff
WHITE = (255, 255, 255)
LIGHT_GRAY = (242, 244, 248)
MID_GRAY = (107, 114, 128)
DARK = (31, 41, 55)
RED = (239, 68, 68)
GREEN = (16, 185, 129)
AMBER = (245, 158, 11)

class CharterPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_auto_page_break(True, margin=20)

    def header(self):
        if self.page_no() == 1:
            return  # Title page has custom header
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 12, 'F')
        self.set_fill_color(*BLUE)
        self.rect(0, 12, 210, 1, 'F')
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(*WHITE)
        self.set_xy(10, 3)
        self.cell(0, 6, 'CLARA-Gainsight Integration Charter  |  v1.0 Draft  |  13 March 2026', 0, 0, 'L')
        self.set_text_color(*DARK)
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*MID_GRAY)
        self.cell(0, 10, f'CLARA-Gainsight Integration Charter  |  DRAFT  |  Page {self.page_no()}', 0, 0, 'R')

    def section_title(self, title):
        # Prevent orphaned headings: if near bottom of page, start new page
        if self.get_y() > 250:
            self.add_page()
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(*NAVY)
        self.cell(0, 10, title, 0, 1)
        self.set_fill_color(*BLUE)
        self.rect(10, self.get_y(), 40, 0.8, 'F')
        self.ln(4)

    def sub_title(self, title):
        if self.get_y() > 260:
            self.add_page()
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*NAVY)
        self.cell(0, 8, title, 0, 1)
        self.ln(1)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bold_body(self, text):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bullet(self, text, bold_prefix=""):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*DARK)
        x = self.get_x()
        self.cell(6, 5, '-', 0, 0)
        if bold_prefix:
            self.set_font('Helvetica', 'B', 10)
            self.cell(self.get_string_width(bold_prefix) + 1, 5, bold_prefix, 0, 0)
            self.set_font('Helvetica', '', 10)
            self.multi_cell(0, 5, text)
        else:
            self.multi_cell(0, 5, text)
        self.ln(1)

    def numbered_item(self, num, title, desc):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*BLUE)
        self.cell(8, 5, str(num) + ".", 0, 0)
        self.set_text_color(*NAVY)
        self.cell(0, 5, title, 0, 1)
        if desc:
            self.set_font('Helvetica', '', 9)
            self.set_text_color(*MID_GRAY)
            self.set_x(self.get_x() + 8)
            self.multi_cell(0, 4.5, desc)
        self.ln(2)

    def add_table(self, headers, rows, col_widths=None):
        w = col_widths or [190 / len(headers)] * len(headers)
        # Ensure header + at least one row fit on current page
        if self.get_y() + 20 > 270:
            self.add_page()
        # Header
        self.set_fill_color(*NAVY)
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', 'B', 9)
        for i, h in enumerate(headers):
            self.cell(w[i], 7, h, 1, 0, 'L', True)
        self.ln()
        # Rows
        self.set_text_color(*DARK)
        for ri, row in enumerate(rows):
            bg = ri % 2 == 0
            if bg:
                self.set_fill_color(*LIGHT_GRAY)
            max_lines = 1
            cell_texts = []
            for ci, cell in enumerate(row):
                lines = self.multi_cell(w[ci], 5, cell, split_only=True)
                cell_texts.append(lines)
                max_lines = max(max_lines, len(lines))
            rh = max_lines * 5 + 2
            # Check page break
            if self.get_y() + rh > 270:
                self.add_page()
                # Redraw header
                self.set_fill_color(*NAVY)
                self.set_text_color(*WHITE)
                self.set_font('Helvetica', 'B', 9)
                for i, h in enumerate(headers):
                    self.cell(w[i], 7, h, 1, 0, 'L', True)
                self.ln()
                self.set_text_color(*DARK)
                if bg:
                    self.set_fill_color(*LIGHT_GRAY)

            y_start = self.get_y()
            x_start = self.get_x()
            for ci, lines in enumerate(cell_texts):
                x = x_start + sum(w[:ci])
                self.set_xy(x, y_start)
                self.set_font('Helvetica', '', 9)
                # Draw cell background
                if bg:
                    self.set_fill_color(*LIGHT_GRAY)
                    self.rect(x, y_start, w[ci], rh, 'F')
                # Draw border
                self.rect(x, y_start, w[ci], rh)
                # Write text
                self.set_xy(x + 1, y_start + 1)
                for line in lines:
                    self.cell(w[ci] - 2, 5, line, 0, 2)
            self.set_y(y_start + rh)
        self.ln(3)

    def draw_arch_diagram(self):
        """Draw the integration architecture diagram."""
        y_base = self.get_y() + 5
        if y_base + 75 > 270:
            self.add_page()
            y_base = self.get_y() + 5

        # Salesforce box
        self.set_fill_color(*LIGHT_GRAY)
        self.set_draw_color(*MID_GRAY)
        self.rect(30, y_base, 45, 15, 'DF')
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(*NAVY)
        self.set_xy(30, y_base + 4)
        self.cell(45, 7, 'Salesforce (CRM)', 0, 0, 'C')

        # Arrow down
        self.set_draw_color(*MID_GRAY)
        self.line(52.5, y_base + 15, 52.5, y_base + 22)
        # Arrowhead
        self.set_fill_color(*MID_GRAY)
        self.polygon([(50, y_base + 20), (55, y_base + 20), (52.5, y_base + 23)], 'F')

        # Gainsight box
        self.set_fill_color(238, 242, 255)
        self.set_draw_color(*BLUE)
        self.set_line_width(0.6)
        self.rect(20, y_base + 24, 65, 28, 'DF')
        self.set_line_width(0.2)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*NAVY)
        self.set_xy(20, y_base + 26)
        self.cell(65, 7, 'Gainsight', 0, 0, 'C')
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*BLUE)
        self.set_xy(20, y_base + 33)
        self.cell(65, 5, 'CSM System of Record', 0, 0, 'C')
        self.set_text_color(*MID_GRAY)
        self.set_xy(20, y_base + 38)
        self.cell(65, 5, 'Health | Engagement | Time Tracking', 0, 0, 'C')
        self.set_xy(20, y_base + 43)
        self.cell(65, 5, 'Use Cases | Blockers | Activities', 0, 0, 'C')

        # CLARA box
        self.set_fill_color(238, 242, 255)
        self.set_draw_color(*NAVY)
        self.set_line_width(0.6)
        self.rect(120, y_base + 24, 65, 28, 'DF')
        self.set_line_width(0.2)
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(*NAVY)
        self.set_xy(120, y_base + 26)
        self.cell(65, 7, 'CLARA', 0, 0, 'C')
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*BLUE)
        self.set_xy(120, y_base + 33)
        self.cell(65, 5, 'Cross-Functional IRP Tracker', 0, 0, 'C')
        self.set_text_color(*MID_GRAY)
        self.set_xy(120, y_base + 38)
        self.cell(65, 5, 'Migration Reporting | Portfolio Reviews', 0, 0, 'C')
        self.set_xy(120, y_base + 43)
        self.cell(65, 5, 'Blockers | Adoption | Action Plans', 0, 0, 'C')

        # Batch arrow (Gainsight -> CLARA)
        batch_y = y_base + 30
        self.set_draw_color(*GREEN)
        self.set_line_width(0.5)
        self.line(85, batch_y, 120, batch_y)
        self.set_fill_color(*GREEN)
        self.polygon([(117, batch_y - 2), (117, batch_y + 2), (120, batch_y)], 'F')
        self.set_line_width(0.2)
        # Batch label
        self.set_fill_color(236, 253, 245)
        self.rect(89, batch_y + 2, 26, 8, 'F')
        self.set_font('Helvetica', '', 7)
        self.set_text_color(5, 150, 105)
        self.set_xy(89, batch_y + 2)
        self.cell(26, 4, 'Batch (S3)', 0, 0, 'C')
        self.set_xy(89, batch_y + 6)
        self.cell(26, 4, 'Accounts, Contacts', 0, 0, 'C')

        # API arrow (bi-directional)
        api_y = y_base + 44
        self.set_draw_color(*BLUE)
        self.set_line_width(0.5)
        self.line(85, api_y, 120, api_y)
        # Left arrowhead
        self.set_fill_color(*BLUE)
        self.polygon([(85, api_y), (88, api_y - 2), (88, api_y + 2)], 'F')
        # Right arrowhead
        self.polygon([(120, api_y), (117, api_y - 2), (117, api_y + 2)], 'F')
        self.set_line_width(0.2)
        # API label
        self.set_fill_color(239, 246, 255)
        self.rect(89, api_y + 2, 26, 8, 'F')
        self.set_font('Helvetica', '', 7)
        self.set_text_color(*BLUE)
        self.set_xy(89, api_y + 2)
        self.cell(26, 4, 'API (Real-time)', 0, 0, 'C')
        self.set_xy(89, api_y + 6)
        self.cell(26, 4, 'Blockers, Tasks, Updates', 0, 0, 'C')

        # App Factory box (bottom center)
        app_y = y_base + 58
        self.set_fill_color(254, 243, 199)
        self.set_draw_color(*AMBER)
        self.rect(85, app_y, 35, 12, 'DF')
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(146, 64, 14)
        self.set_xy(85, app_y + 2)
        self.cell(35, 4, 'App Factory', 0, 0, 'C')
        self.set_font('Helvetica', '', 7)
        self.set_xy(85, app_y + 6)
        self.cell(35, 4, 'Middleware', 0, 0, 'C')

        # Databricks box (bottom left)
        self.set_fill_color(*LIGHT_GRAY)
        self.set_draw_color(*MID_GRAY)
        self.rect(30, app_y, 45, 12, 'DF')
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(*NAVY)
        self.set_xy(30, app_y + 2)
        self.cell(45, 4, 'Databricks', 0, 0, 'C')
        self.set_font('Helvetica', '', 7)
        self.set_text_color(*MID_GRAY)
        self.set_xy(30, app_y + 6)
        self.cell(45, 4, 'Reporting & Analytics', 0, 0, 'C')

        # Arrow Gainsight -> Databricks
        self.set_draw_color(*MID_GRAY)
        self.line(52.5, y_base + 52, 52.5, app_y)
        self.set_fill_color(*MID_GRAY)
        self.polygon([(50, app_y - 2), (55, app_y - 2), (52.5, app_y)], 'F')

        self.set_y(app_y + 18)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)

    def polygon(self, points, style=''):
        """Draw a filled polygon (triangle for arrowheads)."""
        if style == 'F':
            # Use a simple triangle approach
            x1, y1 = points[0]
            x2, y2 = points[1]
            x3, y3 = points[2]
            # fpdf2 polygon
            self._out(f'{x1*self.k:.2f} {(self.h-y1)*self.k:.2f} m')
            self._out(f'{x2*self.k:.2f} {(self.h-y2)*self.k:.2f} l')
            self._out(f'{x3*self.k:.2f} {(self.h-y3)*self.k:.2f} l')
            self._out('f')


def build_pdf(output_path):
    pdf = CharterPDF()

    # --- TITLE PAGE ---
    pdf.add_page()
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_fill_color(*BLUE)
    pdf.rect(0, 180, 210, 2, 'F')

    pdf.set_font('Helvetica', 'B', 36)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(20, 50)
    pdf.multi_cell(170, 18, 'CLARA-Gainsight\nIntegration Charter')

    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(202, 220, 252)
    pdf.set_xy(20, 100)
    pdf.cell(0, 8, 'Version 1.0 (Draft)  |  13 March 2026')

    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(156, 163, 175)
    pdf.set_xy(20, 195)
    pdf.multi_cell(0, 7, 'Author: Azmain Hossain\nCustomer Success Gen AI Programme\nMoody\'s Analytics - Insurance Division')

    # --- Section 1: Purpose ---
    pdf.add_page()
    pdf.section_title('1. Purpose')
    pdf.bold_body('This charter defines the scope, responsibilities, timeline, and success criteria for integrating CLARA with Gainsight.')
    pdf.body_text('It exists to ensure both teams have a shared understanding of what will be built, by whom, and by when - so that no party is surprised by requirements, resource demands, or delivery expectations during execution.')

    # --- Section 2: Background ---
    pdf.section_title('2. Background')
    pdf.bold_body('Gainsight')
    pdf.body_text('System of record for CSMs across Moody\'s Analytics Insurance Division. Provides a unified view of customer health, engagement, time tracking, and BAU activities. CSMs are being onboarded with a production go-live target of 30 March 2026.')
    pdf.bold_body('CLARA')
    pdf.body_text('Internally built web application that tracks IRP adoption and migration across the insurance portfolio. Serves cross-functional teams - CSMs, product, implementation, and advisory - who need visibility into IRP use cases, blockers, adoption milestones, and migration progress. Used in weekly Portfolio Reviews and primary reporting surface for senior leadership.')
    pdf.bold_body('The Problem')
    pdf.body_text('CSMs currently need to work in both systems. Without integration, CSMs must duplicate data entry, and cross-functional teams lose visibility into CSM-side activities.')
    pdf.bold_body('The Goal')
    pdf.body_text('Enable CSMs to work primarily in Gainsight while ensuring IRP adoption data flows seamlessly to CLARA, and that cross-functional inputs captured in CLARA are visible back in Gainsight.')

    # --- Section 3: Parties ---
    pdf.section_title('3. Parties & Stakeholders')
    pdf.sub_title('CLARA Team')
    pdf.add_table(
        ['Name', 'Role'],
        [
            ['Azmain Hossain', 'Programme Manager & Lead Developer, CLARA'],
            ['Ben Brooks', 'Product Owner, CLARA'],
            ['Richard Dosoo', 'Programme & Operational Owner'],
            ['BenVH (Van Houten)', 'Infrastructure Engineer (AWS, CI/CD, App Factory)'],
        ],
        [50, 140]
    )
    pdf.sub_title('Gainsight / Business Systems Team')
    pdf.add_table(
        ['Name', 'Role'],
        [
            ['Tina Palumbo', 'Business Systems, Gainsight Programme Lead'],
            ['Rajesh', 'Solution Architect, Gainsight'],
            ['Shashank', 'Technical Lead, Gainsight Application'],
            ['Nadeem', 'Project Manager, Gainsight Programme'],
        ],
        [50, 140]
    )

    # --- Section 4: Guiding Principles ---
    pdf.section_title('4. Guiding Principles')
    principles = [
        ('Gainsight is the system of record for CSM BAU activities.', 'CSMs should not be required to enter the same data in two systems.'),
        ('CLARA is the system of record for cross-functional IRP adoption tracking.', 'Product, implementation, and advisory teams work in CLARA and should not need Gainsight access.'),
        ('Integration must be bi-directional.', 'Gainsight-originated data must flow to CLARA. CLARA-originated data must flow back to Gainsight.'),
        ('Neither system replaces the other.', 'Gainsight covers the full customer lifecycle. CLARA covers IRP adoption specifically.'),
        ('Start small, prove connectivity, then expand.', 'A POC must demonstrate end-to-end data flow before any production integration is built.'),
        ('No disruption to active migrations.', 'The 2026 insurance scorecard target (30+ migrations) takes priority. Integration work must not divert resources.'),
    ]
    for i, (title, desc) in enumerate(principles):
        pdf.numbered_item(i + 1, title, desc)

    # --- Section 5: Scope ---
    pdf.section_title('5. Scope')

    pdf.sub_title('Phase 1 - Foundation (Accounts & Customer Updates)')
    pdf.add_table(
        ['Source Object', 'CLARA Target', 'Direction', 'Notes'],
        [
            ['Account (Parent + Sub)', 'Parent Accounts / Customers', 'GS -> CLARA', 'Account hierarchy with parent-subsidiary relationships. 155+ active accounts.'],
            ['Customer Weekly Updates', 'Customer Updates', 'Bi-directional', 'Per-account summaries and meeting notes. CLARA auto-generates from transcribed calls. CSMs enter in Gainsight.'],
        ],
        [35, 35, 25, 95]
    )

    pdf.sub_title('Phase 2 - Core IRP Data')
    pdf.add_table(
        ['Source Object', 'CLARA Target', 'Direction', 'Notes'],
        [
            ['Contact / User', 'Employees', 'GS -> CLARA', 'Maps CSMs and key contacts to accounts.'],
            ['Case / Blocker', 'Blockers', 'Bi-directional', 'CSM blockers from Gainsight, product/impl blockers from CLARA.'],
            ['Success Criteria (CSC)', 'Success Criteria', 'Bi-directional', 'IRP use case success criteria tracked by CSMs and product teams.'],
        ],
        [35, 35, 25, 95]
    )

    pdf.sub_title('Phase 3 - Extended Data')
    pdf.add_table(
        ['Source Object', 'CLARA Target', 'Direction', 'Notes'],
        [
            ['Product Adoption (PAT)', 'Product Adoption Tracking', 'GS -> CLARA', 'Adoption milestone data for IRP products.'],
            ['Task / Activity', 'Action Plans / Items', 'Bi-directional', 'Cross-functional action items from both systems.'],
            ['Full Case Feed', 'Case Feed (new table)', 'GS -> CLARA', 'Historical case context for blocker analysis.'],
        ],
        [35, 35, 25, 95]
    )

    pdf.sub_title('Phase 4+ - Future Roadmap')
    pdf.add_table(
        ['Capability', 'Description', 'Dependency'],
        [
            ['Microsoft 365 Context', 'Email + meeting signals per account', 'Graph API access, security review'],
            ['Usage Telemetry (MIDAS)', 'Product usage signals for adoption scoring', 'MIDAS integration, data pipeline'],
            ['NPS Verbatim & CTAs', 'Survey data for sentiment overlay', 'Qualtrics integration'],
            ['Gainsight Health Scores', 'CSM qualitative health (read-only)', 'Gainsight reporting API'],
            ['Write-back to SF/GS', 'Gated future capability', 'Governance framework, security review'],
        ],
        [45, 85, 60]
    )

    # --- Section 6: Architecture ---
    pdf.section_title('6. Integration Architecture')
    pdf.sub_title('Proposed Pattern')
    pdf.body_text('Based on the Gainsight team\'s presentation and technical discussion on 12 March 2026:')
    pdf.draw_arch_diagram()

    pdf.sub_title('Integration Methods')
    pdf.add_table(
        ['Data Type', 'Method', 'Frequency', 'Rationale'],
        [
            ['Account (Parent + Sub)', 'Batch (S3)', 'Daily', 'Low change frequency. Proven and low-risk.'],
            ['Customer Updates', 'API (real-time)', 'On create/update', 'Auto-generated summaries. Timeliness matters.'],
            ['Contact / User', 'Batch (S3)', 'Daily', 'Low change frequency.'],
            ['Blocker', 'API (real-time)', 'On create/update', 'Immediacy needed. Delay causes duplication.'],
            ['Success Criteria', 'API (real-time)', 'On create/update', 'Active during engagements.'],
            ['Product Adoption', 'Batch (S3)', 'Daily', 'Milestone data, not time-critical.'],
            ['Task / Activity', 'API (real-time)', 'On create/update', 'Cross-functional coordination.'],
            ['Case Feed', 'Batch (S3)', 'Daily', 'Historical context.'],
        ],
        [38, 30, 32, 90]
    )

    pdf.sub_title('Authentication & Connectivity')
    pdf.bold_body('Gainsight team will provide:')
    pdf.bullet('API documentation (endpoints, schemas, rate limits, error handling)')
    pdf.bullet('Authentication method and credentials (API key, OAuth, SSO - TBC)')
    pdf.bullet('S3 bucket configuration for batch data exchange')
    pdf.bullet('Sandbox / test environment access for POC')
    pdf.ln(2)
    pdf.bold_body('CLARA team will provide:')
    pdf.bullet('CLARA API specification (REST endpoints for all in-scope objects)')
    pdf.bullet('Authentication details for CLARA\'s API')
    pdf.bullet('Data mapping document (Gainsight field -> CLARA field + transformations)')
    pdf.bullet('Test environment access')
    pdf.ln(2)
    pdf.bold_body('Middleware - App Factory')
    pdf.body_text('Integration orchestration managed through App Factory (CLARA\'s AWS infrastructure). Handles API orchestration, retry logic, data transformation, error logging, and rate limiting. Vendor-agnostic - can be adapted if underlying systems change.')

    # --- Section 7: Responsibilities ---
    pdf.section_title('7. Responsibilities')
    pdf.sub_title('Gainsight / Business Systems Team Owns:')
    for r in ['API documentation and access provisioning', 'S3 bucket setup and configuration for batch exports',
              'Sandbox environment for POC', 'Data export scheduling and reliability (batch jobs)',
              'Webhook / event configuration for real-time sync', 'Data model documentation',
              'CSM change management and training', 'Gainsight-side testing and validation', 'Project management coordination (Nadeem)']:
        pdf.bullet(r)

    pdf.sub_title('CLARA Team Owns:')
    for r in ['API endpoints for receiving and sending data', 'Data transformation and mapping logic',
              'Storage, indexing, and display of Gainsight-sourced data', 'Integration orchestration via App Factory',
              'CLARA-side testing and validation', 'Reporting and dashboards', 'Technical architecture and infrastructure']:
        pdf.bullet(r)

    pdf.sub_title('Joint Responsibilities:')
    for r in ['Data mapping agreement', 'Integration testing (end-to-end)',
              'Error handling and escalation procedures', 'POC evaluation and go/no-go decision',
              'Ongoing monitoring and incident response']:
        pdf.bullet(r)

    # --- Section 8: Success Criteria ---
    pdf.section_title('8. Success Criteria')
    pdf.sub_title('POC Success Criteria')
    poc = [
        ('Connectivity proven:', 'CLARA can authenticate with and read from Gainsight API (or consume S3 exports).'),
        ('Account sync working:', 'At least 10 parent accounts with subsidiaries synced with correct hierarchy.'),
        ('Blocker round-trip:', 'A blocker created in either system appears in the other within 5 minutes.'),
        ('Data integrity:', 'Synced records match - no data loss, no field truncation, no encoding issues.'),
        ('No regression:', 'CLARA\'s existing functionality unaffected by integration.'),
        ('Performance:', 'API responses under 2 seconds. Batch jobs within agreed windows.'),
    ]
    for i, (title, desc) in enumerate(poc):
        pdf.numbered_item(i + 1, title, desc)

    pdf.sub_title('Production Success Criteria')
    prod = [
        'All Phase 1-3 data objects synchronised per schedule.',
        'CSMs can enter IRP data in Gainsight and see it in CLARA without manual intervention.',
        'Cross-functional teams can enter data in CLARA and have it visible in Gainsight.',
        'Zero double-entry for objects covered by integration.',
        'CLARA reporting accurately reflects data from both sources.',
        'Integration uptime of 99.5% during business hours (08:00-18:00 GMT).',
    ]
    for i, p in enumerate(prod):
        pdf.numbered_item(i + 1, p, '')

    # --- Section 9: Timeline ---
    pdf.section_title('9. Timeline')
    pdf.sub_title('Constraints')
    pdf.bullet('Gainsight onboarding deadline: ', '30 March 2026 (RMS, Cape, Predicate teams). No capacity before this.')
    pdf.bullet('Post-launch stabilisation: ', '~4 weeks after go-live (April 2026) for Gainsight to stabilise.')
    pdf.bullet('CLARA graduate onboarding: ', 'Two graduates arriving 7 April 2026. Available from May.')
    pdf.bullet('CLARA team priority: ', '2026 scorecard target (30+ migrations) is primary. Integration is secondary.')

    pdf.sub_title('Proposed Milestones')
    pdf.add_table(
        ['Phase', 'Milestone', 'Target', 'Owner'],
        [
            ['0', 'Charter signed off by both teams', 'TBD', 'Azmain / Tina'],
            ['0', 'GS API documentation shared', 'TBD', 'Rajesh / Shashank'],
            ['0', 'CLARA API spec shared', 'TBD', 'Azmain / BenVH'],
            ['0', 'Data mapping agreed', 'TBD', 'Joint'],
            ['1', 'POC environment setup', 'TBD', 'Joint'],
            ['1', 'POC: Account sync + updates', 'TBD', 'Joint'],
            ['1', 'POC: Real-time blocker sync', 'TBD', 'Joint'],
            ['1', 'POC go/no-go decision', 'TBD', 'Joint + Governance'],
            ['2', 'Phase 2 production build', 'TBD', 'Joint'],
            ['3', 'Phase 3 production build', 'TBD', 'Joint'],
            ['4+', 'Phase 4+ scoping begins', 'TBD', 'Joint'],
        ],
        [15, 75, 20, 80]
    )

    pdf.sub_title('Governance Checkpoints')
    gates = [
        ('Charter Approval', 'Both teams and governance leads sign off.'),
        ('POC Go/No-Go', 'Based on POC success criteria. All six must be met.'),
        ('Phase 2 Go/No-Go', 'Based on POC results and resource availability.'),
        ('Phase 3 Go/No-Go', 'Based on Phase 2 stability and remaining scope.'),
    ]
    for i, (title, desc) in enumerate(gates):
        pdf.numbered_item(i + 1, f'Gate: {title}', desc)

    # --- Section 10: Risks ---
    pdf.section_title('10. Risks & Mitigations')
    risks = [
        ('1', 'HIGH', 'GS API limitations prevent real-time sync', 'POC tests real-time capability. Fallback: near-real-time batch (15 min) via S3.'),
        ('2', 'HIGH', 'Integration diverts CLARA team from migrations', 'Explicitly secondary to scorecard. Governed fortnightly. Graduates from May.'),
        ('3', 'MEDIUM', 'Data model mismatch', 'Mapping agreed before build. Transformation centralised in App Factory.'),
        ('4', 'MEDIUM', 'GS team capacity constrained', 'Timeline accounts for March-April stabilisation. No POC before May.'),
        ('5', 'MEDIUM', 'Bi-directional sync creates conflicts', 'Clear ownership rules. Source system wins. Full audit trail.'),
        ('6', 'MEDIUM', 'Scope creep into Phase 4+', 'Phase 4+ deferred. Additions require governance approval + charter amendment.'),
        ('7', 'MEDIUM', 'Low CSM adoption of GS IRP workflows', 'GS team owns change management. CLARA provides cross-functional docs.'),
        ('8', 'LOW', 'Security review delays', 'Raise requests early (Phase 0). Both teams engage security in parallel.'),
    ]
    pdf.add_table(
        ['#', 'Severity', 'Risk', 'Mitigation'],
        [[r[0], r[1], r[2], r[3]] for r in risks],
        [10, 20, 65, 95]
    )

    # --- Section 11: Change Control ---
    pdf.section_title('11. Change Control')
    pdf.body_text('Any changes to scope, timeline, or responsibilities must:')
    steps = [
        'Be raised in writing (email or shared document comment)',
        'Be reviewed at the next fortnightly governance session',
        'Be agreed by both CLARA lead (Azmain) and Gainsight lead (Tina)',
        'Be approved by governance (Natalia Orzechowska)',
        'Be documented as a charter amendment with version and date',
    ]
    for i, st in enumerate(steps):
        pdf.numbered_item(i + 1, st, '')

    pdf.set_fill_color(254, 226, 226)
    pdf.rect(10, pdf.get_y(), 190, 10, 'F')
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(153, 27, 27)
    pdf.set_xy(15, pdf.get_y() + 2)
    pdf.cell(180, 6, 'No work outside the defined scope will be undertaken without an approved charter amendment.', 0, 0, 'L')
    pdf.ln(15)

    # --- Section 12: Assumptions ---
    pdf.section_title('12. Assumptions')
    assumptions = [
        'Gainsight will have stable API and S3 export capabilities available for the POC.',
        'The Gainsight team will provide dedicated technical resource (Rajesh/Shashank).',
        'CLARA\'s AWS infrastructure (App Factory) can support integration middleware.',
        'Both teams will have sandbox/test environments mirroring production.',
        'CSMs will have been trained on IRP data entry in Gainsight before go-live.',
        'Salesforce data continues to flow into Gainsight and does not need independent sourcing by CLARA.',
    ]
    for i, a in enumerate(assumptions):
        pdf.numbered_item(i + 1, a, '')

    # Version history
    pdf.ln(5)
    pdf.set_fill_color(*LIGHT_GRAY)
    pdf.rect(10, pdf.get_y(), 190, 12, 'F')
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(*MID_GRAY)
    pdf.set_xy(15, pdf.get_y() + 2)
    pdf.cell(0, 4, 'This charter is a living document.', 0, 1)
    pdf.set_xy(15, pdf.get_y())
    pdf.cell(0, 4, 'Version 1.0  |  13 March 2026  |  Azmain Hossain  |  Initial draft', 0, 1)

    pdf.output(output_path)
    print(f"PDF created: {output_path}")


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "CLARA_Gainsight_Integration_Charter_v1.pdf"
    build_pdf(out)
