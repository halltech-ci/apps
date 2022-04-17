odoo.define('expense_management.expense_line_reconcile_action', function (require) {
    'use strict';

    console.log("Module loaded");

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;
    //title: core._t("Lettrage des notes de frais"),

    var ExpenseLineReconcile = AbstractAction.extend({
        title: core._t('Expense Reconciliation'),
        template: 'expense_line',

        init: function(parent, action, options){
            this._super.apply(this, arguments);
            //this._super(parent, action);
            console.log('Module initialized');
            this.action = action;
            this.context = action.context;
            this.actionManager = parent;
            this.options = options || {};
            },
        
        events: {
            //Include events such as click, change, here
            },
    })
    core.action_registry.add('expense_line_reconcile_action', ExpenseLineReconcile);//client action tag:

    return ExpenseLineReconcile;
}
)