

import re
# a search for anything none-alphanumeric and not an underscore
_AN = re.compile('[^\w_]')


from .... import utils
from .. import adminutils

from skipole import FailPage, ValidateError, ServerError, SectionData


def retrieve_managepage(skicall):
    "this call is for the manage special pages page"

    call_data = skicall.call_data
    pd = call_data['pagedata']
    sd = SectionData("adminhead")

    # clears any session data
    adminutils.clear_call_data(call_data)

    project = call_data['editedprojname']
    labeldict = utils.labels(project)

    sd["page_head","large_text"] = "Manage page labels"
    pd.update(sd)

    system_list = utils.sys_list()
    pd['system','col_label'] = system_list
    pd['system','col_input'] = _make_list(project, system_list, labeldict)
    pd['system','hidden_field1'] = system_list

    lib_list = utils.lib_list()
    pd['jq','col_label'] = lib_list
    pd['jq','col_input'] = _make_list(project, lib_list, labeldict)
    pd['jq','hidden_field1'] = lib_list

    user_label_list = [item for item in labeldict if ( (item not in system_list) and (item not in lib_list) )]
    if user_label_list:
        user_label_list.sort()
        pd['user','col_label'] = user_label_list
        pd['user','col_input'] = _make_list(project, user_label_list, labeldict)
        pd['user','hidden_field1'] = user_label_list
    else:
        pd['user','show'] = False



def _make_list(project, reflist, labeldict):
    "Creates a list of url's or string ident numbers of items in reflist"
    result = []
    for item in reflist:
        if item in labeldict:
            target = labeldict[item]
            if isinstance(target, str):
                # its a url
                result.append(target)
            else:
                # its a tuple
                if target[0] == project:
                    result.append(str(target[1]))
                else:
                    result.append(target[0]+','+str(target[1]))
        else:
            result.append('')
    return result


def submit_special_page(skicall):
    "Sets special page"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    label = call_data["label"]
    ident_or_url = call_data["ident_or_url"]
    if (not label) or (not ident_or_url):
        raise FailPage(message = "label or ident missing")

    # check label is valid
    if _AN.search(label):
        raise FailPage(message = "The label can only contain A-Z, a-z, 0-9 and the underscore character.")

    if '_' in label:
        labelparts = label.split('_')
        for lpart in labelparts:
            if lpart.isdigit():
                raise FailPage(message = "Invalid label (Danger of confusion with a page ident, please avoid using digits without letters).")

    if label.isdigit():
        raise FailPage(message = "Invalid label (Danger of confusion with a page ident).")

    try:
        utils.set_label(project, label, ident_or_url)
    except ServerError as e:
        raise FailPage(message = e.message)

    if label in utils.sys_list():
        call_data['status'] = 'System special page %s set' % (label,)
        return
    if label in utils.lib_list():
        call_data['status'] = 'Library special page %s set' % (label,)
        return
    call_data['status'] = 'Label %s set' % (label,)


def add_user_page(skicall):
    "Sets user defined label and target"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    label = call_data["label"]
    ident_or_url = call_data["ident_or_url"]
    if (not label) or (not ident_or_url):
        raise FailPage(message = "label or ident missing", widget='addlabel')

    # check label is valid
    if _AN.search(label):
        raise FailPage(message = "The label can only contain A-Z, a-z, 0-9 and the underscore character.")

    if '_' in label:
        labelparts = label.split('_')
        for lpart in labelparts:
            if lpart.isdigit():
                raise FailPage(message = "Invalid label (Danger of confusion with a page ident, please avoid using digits without letters).")

    if label.isdigit():
        raise FailPage(message = "Invalid label (Danger of confusion with a page ident).")

    if label in utils.lib_list():
        raise FailPage(message = "Invalid label, reserved for system files.")
    if label in utils.sys_list():
        raise FailPage(message = "Invalid label, reserved for system pages.")

    try:
        utils.set_label(project, label, ident_or_url)
    except ServerError as e:
        raise FailPage(message = e.message)
    call_data['status'] = 'Label %s set' % (label,)


def submit_user_page(skicall):
    "Edits or deletes a special user page"

    call_data = skicall.call_data

    project = call_data['editedprojname']
    if 'label' not in call_data:
        raise FailPage(message = "Invalid label.")
    label = call_data["label"]
    if label in utils.lib_list():
        raise FailPage(message = "Invalid label.")
    if label in utils.sys_list():
        raise FailPage(message = "Invalid label.")
    if ("edit" in call_data) and (call_data["edit"]):
        submit_special_page(skicall)
        return
    if ("delete" not in call_data) or (not call_data["delete"]):
        raise FailPage(message = "Invalid submission.")
    try:
        utils.delete_label(project, label)
    except ServerError as e:
        raise FailPage(message = e.message)
    call_data['status'] = 'User label deleted'


