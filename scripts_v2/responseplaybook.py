#!/usr/bin/env python3

from atcutils import ATCutils

from jinja2 import Environment, FileSystemLoader

import os
import re

# ########################################################################### #
# ########################### Response Playboo ############################## #
# ########################################################################### #


class ResponsePlaybook:
    """Class for the Playbook Actions entity"""

    def __init__(self, yaml_file, apipath=None, auth=None, space=None):
        """Init method"""

        # Init vars
        self.yaml_file = yaml_file
        # The name of the directory containing future markdown LogginPolicy
        self.parent_title = "Response_Playbook"

        self.apipath = apipath
        self.auth = auth
        self.space = space

        # Init methods
        self.parse_into_fields(self.yaml_file)

        self.ta_mapping = {
            "attack.initial_access": ("Initial Access", "TA0001"),
            "attack.execution": ("Execution", "TA0002"),
            "attack.persistence": ("Persistence", "TA0003"),
            "attack.privilege_escalation": ("Privilege Escalation", "TA0004"),
            "attack.defense_evasion": ("Defense Evasion", "TA0005"),
            "attack.credential_access": ("Credential Access", "TA0006"),
            "attack.discovery": ("Discovery", "TA0007"),
            "attack.lateral_movement": ("Lateral Movement", "TA0008"),
            "attack.collection": ("Collection", "TA0009"),
            "attack.exfiltration": ("Exfiltration", "TA0010"),
            "attack.command_and_control": ("Command and Control", "TA0011"),
        }

    def parse_into_fields(self, yaml_file):
        """Description"""

        self.rp_parsed_file = ATCutils.read_yaml_file(yaml_file)

    def render_template(self, template_type):
        """Description
        template_type:
            - "markdown"
            - "confluence"
        """

        if template_type not in ["markdown", "confluence"]:
            raise Exception(
                "Bad template_type. Available values:" +
                " [\"markdown\", \"confluence\"]")

        # Point to the templates directory
        env = Environment(loader=FileSystemLoader('templates'))

        # Get proper template
        if template_type == "markdown":
            template = env.get_template(
                'markdown_responseplaybook_template.md.j2'
            )

            tactic = []
            tactic_re = re.compile(r'attack\.\w\D+$')
            technique = []
            technique_re = re.compile(r'attack\.t\d{1,5}$')
            other_tags = []

            for tag in self.rp_parsed_file.get('tags'):
                if tactic_re.match(tag):
                    tactic.append(self.ta_mapping.get(tag))
                elif technique_re.match(tag):
                    technique.append(tag.upper()[7:])
                else:
                    other_tags.append(tag)

            self.rp_parsed_file.update({'tactics': tactic})
            self.rp_parsed_file.update({'techniques': technique})
            self.rp_parsed_file.update({'other_tags': other_tags})

            identification = []
            containment = []
            eradication = []
            recovery = []
            lessons_learned = []

            stages = [
                ('identification', identification),
                ('containment', containment), ('eradication', eradication),
                ('recovery', recovery), ('lessons_learned', lessons_learned)
            ]

            # grab workflow per action in each IR stages
            # error handling for playbooks with empty stages
            for stage_name, stage_list in stages:
                try:
                    for task in self.rp_parsed_file.get(stage_name):
                        action = ATCutils.read_yaml_file(
                            '../response_actions/' + task + '.yml'
                        )

                        stage_list.append(
                            (action.get('description'), action.get('workflow'))
                        )
                except TypeError:
                    pass

            # change stages name to more pretty format
            stages = [(stage_name.replace('_', ' ').capitalize(),
                       stage_list) for stage_name, stage_list in stages]

            self.rp_parsed_file.update({'stages': stages})

            self.rp_parsed_file.update(
                {'description': self.rp_parsed_file
                    .get('description').strip()}
            )

        elif template_type == "confluence":
            template = env.get_template(
                'confluence_responseplaybook_template.html.j2'
            )

            tactic = []
            tactic_re = re.compile(r'attack\.\w\D+$')
            technique = []
            technique_re = re.compile(r'attack\.t\d{1,5}$')
            other_tags = []

            for tag in self.rp_parsed_file.get('tags'):
                if tactic_re.match(tag):
                    tactic.append(self.ta_mapping.get(tag))
                elif technique_re.match(tag):
                    technique.append(tag.upper()[7:])
                else:
                    other_tags.append(tag)

            self.rp_parsed_file.update({'tactics': tactic})
            self.rp_parsed_file.update({'techniques': technique})
            self.rp_parsed_file.update({'other_tags': other_tags})

            # get links to response action

            identification = []
            containment = []
            eradication = []
            recovery = []
            lessons_learned = []

            stages = [
                ('identification', identification),
                ('containment', containment), ('eradication', eradication),
                ('recovery', recovery), ('lessons_learned', lessons_learned)
            ]

            for stage_name, stage_list in stages:
                try:
                    for task in self.rp_parsed_file.get(stage_name):
                        action = ATCutils.read_yaml_file(
                            '../response_actions/' + task + '.yml'
                        )
                        action_title = action.get('title')
                        if self.apipath and self.auth and self.space:
                            stage_list.append(
                                (action_title,
                                 str(ATCutils.get_page_id(
                                     self.apipath, self.auth,
                                     self.space, action_title)
                                     )
                                 )
                            )
                        else:
                            stage_list.append((action_title, ""))

                except TypeError:
                    pass

            # change stages name to more pretty format
            stages = [(stage_name.replace('_', ' ').capitalize(), stage_list)
                      for stage_name, stage_list in stages]

            self.rp_parsed_file.update({'stages_with_id': stages})

            # get descriptions for response actions

            identification = []
            containment = []
            eradication = []
            recovery = []
            lessons_learned = []

            stages = [
                ('identification', identification),
                ('containment', containment), ('eradication', eradication),
                ('recovery', recovery), ('lessons_learned', lessons_learned)
            ]

            # grab workflow per action in each IR stages
            # error handling for playbooks with empty stages
            for stage_name, stage_list in stages:
                try:
                    for task in self.rp_parsed_file.get(stage_name):
                        action = ATCutils.read_yaml_file(
                            '../response_actions/' + task + '.yml')
                        stage_list.append(
                            (action.get('description'),
                             action.get('workflow') + '    \n\n.')
                        )
                except TypeError:
                    pass

            # change stages name to more pretty format
            stages = [(stage_name.replace('_', ' ').capitalize(), stage_list)
                      for stage_name, stage_list in stages]

            self.rp_parsed_file.update({'stages': stages})

            self.rp_parsed_file.update(
                {'description': self.rp_parsed_file
                    .get('description').strip()}
            )

        # Render
        self.content = template.render(self.rp_parsed_file)

    def save_markdown_file(self, atc_dir='../Atomic_Threat_Coverage/'):
        """Write content (md template filled with data) to a file"""

        base = os.path.basename(self.yaml_file)
        title = os.path.splitext(base)[0]

        file_path = atc_dir + self.parent_title + "/" + \
            title + ".md"

        return ATCutils.write_file(file_path, self.content)
