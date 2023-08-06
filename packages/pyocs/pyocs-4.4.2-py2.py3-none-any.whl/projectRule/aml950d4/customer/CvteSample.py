from projectRule.aml950d4.Aml950d4Common import Aml950d4Common
from customers.customer_common.common_database import commonDataBase

class Ruler(Aml950d4Common):

    # Customer_ID
    _customer_id = 'CUSTOMER_SAMPLE_AUTO_CONFIG'

    # 代码分支
    _code_branch = ""

    # 测试类型
    _test_type = 'F'

    def get_ocs_modelid(self):
        project = self.request_dict[self.ocs_demand.product_name].replace('.', '_')
        modelid = 'CS' + self.ocs_number + '_SAMPLE_' + project + '_ID_PNL_GENERAL' \
                  + '_DUTY_' + self.request_dict[self.ocs_demand.pwm_name]
        return modelid

    def get_ocs_require(self):
        """获取ocs上的配置，生成配置代码
        Args:
            ocs_number：OCS订单号
        Returns:
             返回配置代码
        """
        ret = ''
        _space = 60
        ret += '#elif ( IsModelID('+ self.get_ocs_modelid() + ') )' + '\n'
        ret += '//ocs ID & board & chip & flash & sound' + '\n'
        ret += self.get_board_macro()
        ret += self.get_chip_macro()
        # ret += self.get_ddr_macro()
        ret += self.get_flash_size_macro()
        ret += '//ci' + '\n'
        ret += self.get_ci_macro()
        ret += '//tuner' + '\n'
        ret += self.get_tuner_macro()
        ret += '//country' + '\n'
        ret += self.get_ocs_country()
        ret += '//logo & ir & keypad' + '\n'
        ret += self.get_macro_line("CVT_DEF_LOGO_TYPE", "ID_LOGO_COMMON_DEFAULT")
        ret += self.get_macro_line("CVT_DEF_IR_TYPE", "ID_IR_CVTE_AM_KA80")
        ret += self.get_macro_line("CVT_DEF_KEYPAD_TYPE", "ID_KEYPAD_CVTE_7KEY_COMMON_DEFAULT")
        ret += self.get_macro_line("CVT_DEF_KEYPAD_ADC", "ID_KEYPAD_ADC_COMMON_DEFAULT")
        ret += '//panel & pq & ref' + '\n'
        ret += self.get_macro_line("CVT_DEF_PANEL_TYPE", "ID_PNL_GENERAL_1920_1080")
        ret += self.get_macro_line("CVT_DEF_PANEL_NAME", "\"GENERAL_1920_1080\"")
        ret += self.get_pwm_macro()
        ret += self.get_eshare_macro()
        ret += self.get_wifi_macro()
        ret += self.get_bluetooth_macro()

        ret += '//menu config & launcher' + '\n'
        other_app_list = self.request_dict[self.ocs_demand.other_app_soft]
        if other_app_list and 'GAIA' in other_app_list:
            ret += self.get_macro_line("CVT_DEF_LAUNCHER_TYPE", "ID_LAUNCHER_40_GAIA_30_MOSAIX")
        else:
            ret += self.get_macro_line("CVT_DEF_LAUNCHER_TYPE", "ID_LAUNCHER_40_SATURN")

        if other_app_list and 'Eshare' in other_app_list:
            pass

        ret += '// end\n'
        return ret

    def get_ocs_country(self):
        ret = ''
        ret += self.get_macro_line("CVT_DEF_COUNTRY_SELECT", "ID_COUNTRY_TURKEY")
        return ret