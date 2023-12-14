frappe.ui.form.on("Saudi Zatca settings", {
    refresh: function(frm) {
        frm.add_custom_button(__("click"), function() {
            frm.call({
                method: "saudi_phase2_api.saudi_phase2_api.csrcode.zatca_csr",
                callback: function(response) {
                    if (response.message) {  
                        frappe.msgprint(response.message);
                    }
                }
            });
        }, __("create csr"));
    }
});
