# Copyright 2022 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from collections import defaultdict

from ebi_eva_common_pyutils.config_utils import get_primary_mongo_creds_for_profile, get_accession_pg_creds_for_profile, \
    get_count_service_creds_for_profile, get_properties_from_xml_file


class SpringPropertiesGenerator:
    """
    Class to generate Spring properties for various Spring Batch pipelines.
    These methods can be used to generate complete properties files entirely in Python; alternatively, certain
    properties can be left unfilled and supplied as command-line arguments (e.g. by a NextFlow process).
    """

    def __init__(self, maven_profile, private_settings_file):
        self.maven_profile = maven_profile
        self.private_settings_file = private_settings_file

    @staticmethod
    def _format(*key_value_maps):
        all_params = defaultdict(list)
        for key_value_map in key_value_maps:
            for key in key_value_map:
                if key_value_map[key] is not None:
                    all_params[key.split('.')[0]].append(f'{key}={key_value_map[key]}')
        lines = []
        for key_type in all_params:
            for line in all_params[key_type]:
                lines.append(line)
            lines.append('')

        return '\n'.join(lines)

    @staticmethod
    def _format_str(string, param):
        if param is None:
            return None
        elif not param:
            return ''
        else:
            return string.format(param)

    def _common_properties(self, *, assembly_accession, read_preference='primary', chunk_size=100):
        """Properties common to all Spring pipelines"""
        mongo_host, mongo_user, mongo_pass = get_primary_mongo_creds_for_profile(
            self.maven_profile, self.private_settings_file)
        pg_url, pg_user, pg_pass = get_accession_pg_creds_for_profile(self.maven_profile, self.private_settings_file)
        accession_db = get_properties_from_xml_file(
            self.maven_profile, self.private_settings_file)['eva.accession.mongo.database']
        return {
            'spring.datasource.driver-class-name': 'org.postgresql.Driver',
            'spring.datasource.url': pg_url,
            'spring.datasource.username': pg_user,
            'spring.datasource.password': pg_pass,
            'spring.datasource.tomcat.max-active': 3,
            'spring.jpa.generate-ddl': 'true',
            'spring.data.mongodb.host': mongo_host,
            'spring.data.mongodb.port': 27017,
            'spring.data.mongodb.database': accession_db,
            'spring.data.mongodb.username': mongo_user,
            'spring.data.mongodb.password': mongo_pass,
            'spring.data.mongodb.authentication-database': 'admin',
            'mongodb.read-preference': read_preference,
            'spring.main.web-application-type': 'none',
            'spring.main.allow-bean-definition-overriding': 'true',
            'spring.jpa.properties.hibernate.jdbc.lob.non_contextual_creation': 'true',
            'parameters.chunkSize': chunk_size,
            'parameters.assemblyAccession': assembly_accession,
        }

    def _accessioning_properties(self, *, instance=''):
        """Properties common to accessioning and clustering pipelines."""
        counts_url, counts_username, counts_password = get_count_service_creds_for_profile(
            self.maven_profile, self.private_settings_file)

        return {
            'accessioning.instanceId': self._format_str('instance-{0}', instance),
            'accessioning.submitted.categoryId': 'ss',
            'accessioning.clustered.categoryId': 'rs',
            'accessioning.monotonic.ss.blockSize': 100000,
            'accessioning.monotonic.ss.blockStartValue': 5000000000,
            'accessioning.monotonic.ss.nextBlockInterval': 1000000000,
            'accessioning.monotonic.rs.blockSize': 100000,
            'accessioning.monotonic.rs.blockStartValue': 3000000000,
            'accessioning.monotonic.rs.nextBlockInterval': 1000000000,
            'eva.count-stats.url': counts_url,
            'eva.count-stats.username': counts_username,
            'eva.count-stats.password': counts_password
        }

    def get_accessioning_properties(self, *, instance=None, target_assembly=None,  fasta=None, assembly_report=None,
                                    project_accession=None, aggregation='BASIC', taxonomy_accession=None,
                                    vcf_file='', output_vcf='', chunk_size=100):
        """Properties for accessioning pipeline."""
        return self._format(
            self._common_properties(assembly_accession=target_assembly, read_preference='secondaryPreferred',
                                    chunk_size=chunk_size),
            self._accessioning_properties(instance=instance),
            {
                'spring.batch.job.names': 'CREATE_SUBSNP_ACCESSION_JOB',
                'parameters.assemblyReportUrl': self._format_str('file:{0}', assembly_report),
                'parameters.contigNaming': 'NO_REPLACEMENT',
                'parameters.fasta': fasta,
                'parameters.forceRestart': 'false',
                'parameters.projectAccession': project_accession,
                'parameters.taxonomyAccession': taxonomy_accession,
                'parameters.vcfAggregation': aggregation,
                'parameters.vcf': vcf_file,
                'parameters.outputVcf': output_vcf
            },
        )

    def get_remapping_extraction_properties(self, *, taxonomy=None, source_assembly=None, fasta=None,
                                            assembly_report=None,
                                            projects='', output_folder=None):
        """Properties for remapping extraction pipeline."""
        return self._format(
            self._common_properties(assembly_accession=source_assembly, read_preference='secondaryPreferred',
                                    chunk_size=1000),
            {
                'spring.batch.job.names': 'EXPORT_SUBMITTED_VARIANTS_JOB',
                'parameters.taxonomy': taxonomy,
                'parameters.fasta': fasta,
                'parameters.assemblyReportUrl': self._format_str('file:{0}', assembly_report),
                'parameters.projects': projects,
                'parameters.outputFolder': output_folder
            })

    def get_remapping_ingestion_properties(self, *, source_assembly=None, target_assembly=None, vcf=None, load_to=None,
                                           remapping_version=1.0):
        """Properties for remapping ingestion pipeline."""
        return self._format(
            self._common_properties(assembly_accession=target_assembly, read_preference='secondaryPreferred',
                                    chunk_size=1000),
            {
                'spring.batch.job.names': 'INGEST_REMAPPED_VARIANTS_FROM_VCF_JOB',
                'parameters.vcf': vcf,
                'parameters.remappedFrom': source_assembly,
                'parameters.loadTo': load_to,
                'parameters.remappingVersion': remapping_version,
            }
        )

    def get_clustering_properties(self, *, instance=None, read_preference='primary',
                                  job_name=None, source_assembly='', target_assembly='', rs_report_path='', projects='',
                                  project_accession='', vcf=''):
        """Properties common to all clustering pipelines, though not all are always used."""
        return self._format(
            self._common_properties(assembly_accession=target_assembly, read_preference=read_preference,
                                    chunk_size=100),
            self._accessioning_properties(instance=instance),
            {
                'spring.batch.job.names': job_name,
                'parameters.remappedFrom': source_assembly,
                'parameters.projects': projects,
                'parameters.projectAccession': project_accession,
                'parameters.vcf': vcf,
                'parameters.rsReportPath': rs_report_path
            }
        )

    def get_release_properties(self, *, job_name=None, assembly_accession=None, fasta=None, assembly_report=None,
                               contig_naming=None, output_folder=None, accessioned_vcf=None):

        return self._format(
            self._common_properties(assembly_accession=assembly_accession, read_preference='secondaryPreferred',
                                    chunk_size=1000),
            {
                'spring.batch.job.names': job_name,
                'parameters.contigNaming': contig_naming,
                'parameters.fasta': fasta,
                'parameters.assemblyReportUrl': self._format_str('file:{0}', assembly_report),
                'parameters.outputFolder': output_folder,
                'parameters.accessionedVcf': accessioned_vcf,
                'logging.level.uk.ac.ebi.eva.accession.release': 'INFO'
            })
