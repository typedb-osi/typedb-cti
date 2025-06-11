from stix_model.loaders import PropertyMappings

##### Embedded Relationships #####
##### Note: these are intended to be used with the 'self' role direction only #####

embedded_created_by_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="created_by_ref",
		player_attribute="id",
		relation_type="created-by",
		self_role="created",
		player_role="creator",
		quoted=True
	)

embedded_object_marking_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="object_marking_refs",
		player_attribute="id",
		relation_type="object-marking",
		self_role="object",
		player_role="marking",
		quoted=True,
	)

# TODO: granular marking

embedded_object_reference_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="object_refs",
		player_attribute="id",
		relation_type="object-reference",
		self_role="referencing-group",
		player_role="referenced-object",
		quoted=True,
	)

# TODO: meta-object-reference

embedded_host_vm_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="host_vm_ref",
		player_attribute="id",
		relation_type="host-vm",
		self_role="hosted",
		player_role="host",
		quoted=True
	)

embedded_operating_system_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="operating_system_ref",
		player_attribute="id",
		relation_type="operating-system",
		self_role="hosted",
		player_role="os",
		quoted=True
	)

embedded_installed_software_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="installed_software_refs",
		player_attribute="id",
		relation_type="installed-software",
		self_role="hosted",
		player_role="software",
		quoted=True,
	)

embedded_analysis_sco_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="analysis_sco_refs",
		player_attribute="id",
		relation_type="analysis-sco",
		self_role="analyzed",
		player_role="analysis",
		quoted=True,
	)

embedded_sample_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="sample_ref",
		player_attribute="id",
		relation_type="sample",
		self_role="source",
		player_role="sample",
		quoted=True
	)

embedded_contains_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="contains_refs",
		player_attribute="id",
		relation_type="contains_",
		self_role="container",
		player_role="contained",
		quoted=True
	)

embedded_header_from_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="from_ref",
		player_attribute="id",
		relation_type="header-from",
		self_role="email",
		player_role="address",
	)

embedded_header_sender_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="sender_ref",
		player_attribute="id",
		relation_type="header-sender",
		self_role="email",
		player_role="address",
	)

embedded_header_to_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="to_refs",
		player_attribute="id",
		relation_type="header-to",
		self_role="email",
		player_role="address",
	)

embedded_header_cc_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="cc_refs",
		player_attribute="id",
		relation_type="header-cc",
		self_role="email",
		player_role="address",
	)

embedded_header_bcc_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="bcc_refs",
		player_attribute="id",
		relation_type="header-bcc",
		self_role="email",
		player_role="address",
	)

embedded_raw_email_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="raw_email_ref",
		player_attribute="id",
		relation_type="raw-email",
		self_role="email",
		player_role="artifact",
	)

# TODO: use after http request extension is finished
embedded_message_body_data_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="message_body_data_ref",
		player_attribute="id",
		relation_type="message-body-data",
		self_role="request",
		player_role="body",
	)

embedded_file_content_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="content_ref",
		player_attribute="id",
		relation_type="file-content",
		self_role="file",
		player_role="content",
	)

# TODO: after windows-service-ext extension is finished
embedded_service_dll_properties = PropertyMappings() \
	.relation_existing_player(
		player_attribute_doc_key="service_dll_refs",
		player_attribute="id",
		relation_type="service-dll",
		self_role="service",
		player_role="dll",
	)