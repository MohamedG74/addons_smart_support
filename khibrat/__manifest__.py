{
    'name': 'Khibrat',
    'version': '16.0.0.0',
    'category': '',
    'summary': '.',
    'description': """
      
""",
    'author': 'SmartSupport',
    'website': 'https://www.smartsupport.tech',
    'depends': ['base','mail'],
    'data': [
        'data/sequence.xml',
        'data/mail_template_data.xml',
        'data/start_end_date_in_cases.xml',
        'data/lawyers_agency_end_date.xml',
        'data/consultants_agency_end_date.xml',
        'data/primary_judgment_end_date.xml',
        'data/appellate_judgment_end_date.xml',
        'data/cases_to_lawyers_consultants_client.xml',
        'data/cases_to_lawyers_consultants_defendant.xml',
        'for_security/ir.model.access.csv',    
        'views/menus.xml',
        'views/lawyers.xml',
        'views/clients.xml',
        'views/courts.xml',
        'views/case_type.xml',
        'views/defendant.xml',
        'views/cases.xml',
        'views/document.xml',
        'views/demands.xml',
        'views/session.xml',
        'views/interfering.xml',
        'views/entries.xml',
        'views/experts.xml',
        'views/witness.xml',
        'views/reservation.xml',
        'views/another_decision.xml',
        'views/primary_judgment.xml',
        'views/appellate_judgment.xml',
        'views/final_requests.xml',
        'views/final_judgment.xml',
        'views/exchange_notes.xml',
        'views/expert_installments.xml',
        'views/consultants.xml',
        'views/session_report.xml',
        'views/appellate_judgment_second.xml',
        'views/final_judgment_second.xml',
        'views/legal_consultations_and_studies.xml',
        
    ],
    'assets': {
        'web.assets_backend': [
            'khibrat/static/src/scss/khibrat.scss',
        ],
    },

    'installable': True,
    'auto_install': False,
    "images":[],
}
