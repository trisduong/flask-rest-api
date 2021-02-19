from flask_restful import Resource, reqparse
from models.orderdetails import OrderdetailModel
from flask import request, current_app, jsonify, url_for


class Orderdetails(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('quantityOrdered',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('priceEach',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('orderLineNumber',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, orderdetailkey):
        orderdetail = OrderdetailModel.find_by_orderNumber(orderdetailkey)
        if orderdetail:
            return orderdetail.json()
        else:
            orderdetail = OrderdetailModel.find_by_productCode(orderdetailkey)
            if orderdetail:
                return  orderdetail.json()
            else:
                return {'message': 'orderdetail not found'}, 404

    def post(self, orderdetailkey):
        if OrderdetailModel.find_by_orderNumber(orderdetailkey):
            return {'message': f'A orderdetail with orderNumber: {orderNumber} already exists'}, 400

        if OrderdetailModel.find_by_productCode(orderdetailkey):
            return {'message': f'A orderdetail with productCode: {productCode} already exists'}, 400

        data = Orderdetails.parser.parse_args()

        orderdetail = OrderdetailModel(orderdetailkey, **data)

        try:
            orderdetail.save_to_db()
        except:
            return {"message": "An Error occurred inserting the orderdetail."}, 500

        return {"message": "office added successful."}, 201

    def delete(self, orderdetailkey):
        orderdetail = OrderdetailModel.find_by_orderNumber(orderdetailkey)
        if orderdetail:
            orderdetail.delete_from_db()
            return {'message': 'orderdetail deleted'}
        else:
            orderdetail = OrderdetailModel.find_by_productCode(orderdetailkey)
            if orderdetail:
                orderdetail.delete_from_db()
                return {'message': 'orderdetail deleted'}
            else:
                return {'message': 'orderdetail not found'}, 404

    def put(self, orderdetailkey):
        data = Orderdetails.parser.parse_args()

        orderdetail = OrderdetailModel.find_by_orderNumber(orderdetailkey)
        if orderdetail:
            orderdetail.delete_from_db()
            orderdetail = OrderdetailModel(orderdetailkey, **data)
        else:
            orderdetail = OrderdetailModel.find_by_productCode(orderdetailkey)
            if orderdetail:
                orderdetail.delete_from_db()
                orderdetail = OrderdetailModel(orderdetailkey, **data)
            else:
                orderdetail = OrderdetailModel(orderdetailkey, **data)

        orderdetail.save_to_db()

        return {"message": "office alter successful."}


class OrderdetailList(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        pagination = OrderdetailModel.query.paginate(
            page, per_page=current_app.config['REST_POSTS_PER_PAGE'],
            error_out=False)
        orderdetails = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('orderdetaillist', page=page - 1)
        next = None
        if pagination.has_next:
            next = url_for('orderdetaillist', page=page + 1)
        return jsonify({
            'orderdetails': [orderdetail.json() for orderdetail in orderdetails],
            'prev': prev,
            'next': next,
            'Total count': pagination.total,
            'Page count': current_app.config['REST_POSTS_PER_PAGE'],
        })
