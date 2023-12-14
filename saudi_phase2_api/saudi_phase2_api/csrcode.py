
import frappe
# frappe.init(site="husna.erpgulf.com")
# frappe.connect()
import subprocess
import base64
import json
import sys
import requests

def generate_csr():
                settings=frappe.get_doc('Saudi Zatca settings')
                csr_config_file = 'sdkcsrconfig.properties'
                private_key_file = 'sdkprivatekey.pem'
                generated_csr_file = 'sdkcsr.pem'
                command_generate_csr = f'fatoora -csr -csrConfig {csr_config_file} -privateKey {private_key_file} -generatedCsr {generated_csr_file} -pem'
                try:
                    subprocess.run(command_generate_csr, shell=True, check=True, text=True)
                    with open("generated-csr-20231211124058.csr", "r") as file_csr:
                        get_csr = file_csr.read()
                    file = frappe.get_doc(
                        {
                            "doctype": "File",
                            "file_name": f"generated-csr-{settings.name}.csr",
                            "attached_to_doctype": settings.doctype,
                            "attached_to_name": settings.name,
                            "content": get_csr,


                        }
                    )
                    file.save()
                    get_csr = get_csr.strip()
                    encoded_certificate = base64.b64encode(get_csr.encode("utf-8")).decode("utf-8")
                    with open("encoded_csr.txt", "w") as file:
                        file.write(encoded_certificate)
                    return f"CSR generation successful. CSR saved as {generated_csr_file}"
                except subprocess.CalledProcessError as e:
                    return f"Error: {e.stderr}"

def csr_Attach():       
            frappe.msgprint("hello")
            # with open ("encoded_csr.txt" , "r") as read_file :        
            #     json_data = {
            #         'csr': read_file.read(),}
            # frappe.msgprint(json_data)  
                    
#             response = requests.post(
#                 'https://gw-fatoora.zatca.gov.sa/e-invoicing/developer-portal/compliance',
#                 headers=headers,
#                 json=json_data, )
#             print(response)
#             if response.status_code == 200:
#                 try:
#                 # Try to parse JSON
#                      data = json.loads(response.text)
#                 # Continue with processing data
#                 except json.JSONDecodeError as e:
#                     print(f"Error decoding JSON: {e}")
#                 # Handle the error or return None, depending on your use case
#                     sys.exit()
#                 final_resp = json.dumps(data)
#                 with open("response_from_send_csr.json", "w") as file:
#                     file.write(final_resp)
#                 binary_security_token = data.get("binarySecurityToken")
#                 secret = data.get("secret")
#                 if binary_security_token and secret:
#                     print("Binary Security Token:", binary_security_token)
#                     print("Secret:", secret)
#             # Optionally, you can return these values or perform additional actions
#             # return binary_security_token, secret
# #             else:
# #                 print(f"HTTP request failed with status code: {response.status_code}")
           
# # # generate_csr()
# # send_csr()

@frappe.whitelist(allow_guest=True)
def zatca_csr():
                frappe.msgprint("inside zatca baground")
                csr_Attach()




def create_security_token_from_csr():
            try:
                with open("generated-csr-20231211124058.csr", "r") as f:
                            csr_contents = f.read()
            except Exception as e:
                        print(str(e))
            base64csr = base64.b64encode(csr_contents.encode("utf-8")).decode("utf-8")
            url = "https://gw-fatoora.zatca.gov.sa/e-invoicing/developer-portal/compliance"
            payload = json.dumps({
            "csr": base64csr
            })
            headers = {
            'accept': 'application/json',
            'OTP': '123345',
            'Accept-Version': 'V2',
            'Content-Type': 'application/json',
            'Cookie': 'TS0106293e=0132a679c07382ce7821148af16b99da546c13ce1dcddbef0e19802eb470e539a4d39d5ef63d5c8280b48c529f321e8b0173890e4f'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            data=json.loads(response.text)
            print(response)
            return data["binarySecurityToken"],  data["secret"]
