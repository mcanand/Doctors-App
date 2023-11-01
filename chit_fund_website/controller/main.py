from odoo import http,api
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class MyHomepage(http.Controller):

    @http.route('/', type='http', auth='public', website=True)
    def homepagedet(self, **kwargs):
        chit_funds = request.env['chit.fund'].sudo().search([('state', '=', 'draft')])
        chit_items = []
        for chit in chit_funds:
            chit_item = {
                'name': chit.name,
                'amount': chit.amount,
                'start_date': chit.start_date,
                'end_date': chit.end_date,
                'span': chit.span,
                'amount_payable': chit.amount_payable,
                'lucky_draw_till': chit.lucky_draw_till,
            }
            chit_items.append(chit_item)
            active_chits = request.env['chit.fund'].search_count([('state', '=', 'in_progress')])
            new_chits = request.env['chit.fund'].search_count([('state', '=', 'draft')])
            waiting_chits = request.env['chit.fund'].search_count(
                [('state', '=', 'draft')])
            all_chits = request.env['chit.fund'].search_count([])




        return request.render('chit_fund_website.website_my_homepage',{'chit_items':chit_items, 'active_chits': active_chits,
                'new_chits': new_chits,
                'waiting_chits': waiting_chits,
                'all_chits': all_chits,})

    @http.route('/d', type='http', auth="public", website=True)
    def submit_enquiry(self, **kw):
        name = kw.get('name')
        print(name)
        phone =kw.get('phone')
        email_from = kw.get('email_from')


        chit_enquiry = request.env['chit.enquiry'].sudo().create({
            'name': name,
            'phone': phone,
            'email': email_from,
        })
        return request.redirect('/')

    @http.route('/submit/data', type='http', auth="public", website=True)
    def submit_data(self, **kw):
        name = kw.get('name')
        phone = kw.get('phone')
        email_from = kw.get('email')
        is_checked = kw.get('click')

        chit_enquiry = request.env['chit.enquiry'].sudo().create({
            'name': name,
            'phone': phone,
            'email': email_from,
            'confirm':is_checked,
        })

        return request.redirect('/')



class MyDashboard(CustomerPortal):

    @http.route(['/my/history'], type='http', auth='user', website=True, methods=['GET', 'POST'])
    def my_history(self, **kw):
        partner_id = request.env.user.partner_id.id
        active_chits = request.env['chit.fund'].sudo().search(
            [('state', '=', 'done')])
        history_chit_list = []

        for chit in active_chits:
            chit_details = {
                'name': chit.name,
                'amount': chit.amount,
                'id':chit.id,

            }
            history_chit_list.append(chit_details)
        print(active_chits)
        return request.render('chit_fund_website.portal_my_home_inherit',{'history_chit_list': history_chit_list} )



    @http.route(['/active/chit/details'], type='http', auth='user', website=True,
                methods=['GET', 'POST'])
    def active_chit_details(self, **kw):
        partner_id = request.env.user.partner_id.id
        active_chits = request.env['chit.fund'].sudo().search([('state','=', 'in_progress')])
        active_chit_list = []

        for chit in active_chits:
            chit_details = {
                'name': chit.name,
                'amount': chit.amount,
                'id':chit.id,

            }
            active_chit_list.append(chit_details)
        print(active_chits)
        return request.render('chit_fund_website.portal_my_membership_upgrade', {'active_chit_list': active_chit_list,})


    @http.route(['/upcoming/chits'], type='http', auth='user', website=True,
                methods=['GET', 'POST'])
    def upcoming_chits(self, **kw):
        partner_id = request.env.user.partner_id.id
        active_chits = request.env['chit.fund'].sudo().search([('state', '=', 'draft')])
        chit_details_list = []

        for chit in active_chits:
            chit_details = {
                'name': chit.name,
                'amount': chit.amount,
                'id':chit.id,

            }
            chit_details_list.append(chit_details)
        return request.render('chit_fund_website.portal_my_upcoming_chits', {'chit_details_list': chit_details_list,})

    @http.route('/upcoming/chits/details/<int:chit_id>', auth='public', website=True)
    def chit_fund_details(self, chit_id, **kwargs):
        chit_fund = request.env['chit.fund'].browse(chit_id)
        partner_id= request.env.user.partner_id.id
        return request.render('chit_fund_website.chit_fund_details_template',{'chit_fund': chit_fund,
        })


    @http.route('/active/chits/data/<int:chit_id>', auth='public', website=True)
    def chit_active_detail(self, chit_id, **kwargs):
        print('xxx')
        chit_fund = request.env['chit.fund'].browse(chit_id)
        partner_id = request.env.user.partner_id.id
        monthly_amount = request.env['chit.month'].search(
            [('chit_fund_id', '=', chit_id)])
        monthly_amounts = []

        for amount in monthly_amount:
            chit_details = {
                'month': amount.name,
                'winner': amount.chit_partner_id.name,
                'draw_type':amount.draw_type,
                'payable' :amount.payable,
                'won_amount' : amount.won_amount,
                'paid' : bool(amount.chit_month_bid_ids)

            }
            monthly_amounts.append(chit_details)
        return request.render('chit_fund_website.active_chit_fund_details_template',
                              {'chit_fund': chit_fund, 'monthly_amounts': monthly_amounts,
                               })

    @http.route('/chits/history/details/<int:chit_id>', auth='public', website=True)
    def chit_history_details(self, chit_id, **kwargs):
        chit_fund = request.env['chit.fund'].browse(chit_id)
        partner_id = request.env.user.partner_id.id
        monthly_amount = request.env['chit.month'].search(
            [('chit_fund_id', '=', chit_id)])
        monthly_amounts = []

        for amount in monthly_amount:
            chit_details = {
                'month': amount.name,
                'winner': amount.chit_partner_id.name,
                'draw_type': amount.draw_type,
                'payable': amount.payable,
                'won_amount': amount.won_amount,
                'paid': bool(amount.chit_month_bid_ids)

            }
            monthly_amounts.append(chit_details)
        return request.render('chit_fund_website.history_chit_fund_details_template',
                              {'chit_fund': chit_fund, 'monthly_amounts': monthly_amounts,
                               })

