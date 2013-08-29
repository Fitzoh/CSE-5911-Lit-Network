hugo_gene_symbols
=================

Convert putative gene symbols to official HUGO gene symbols. Confirm that a symbol is a HUGO symbol in the correct case.

HUGO Download page (last downloaded May 21, 2013)
http://www.genenames.org/cgi-bin/hgnc_downloads

Download command:

wget "http://www.genenames.org/cgi-bin/hgnc_downloads?col=gd_hgnc_id&col=gd_app_sym&col=gd_app_name&col=gd_status&col=gd_prev_sym&col=gd_aliases&col=gd_pub_chrom_map&col=gd_date_mod&col=gd_pub_acc_ids&col=gd_pub_eg_id&col=gd_pub_ensembl_id&col=gd_pub_refseq_ids&col=md_prot_id&status=Approved&status=Entry+Withdrawn&status_opt=2&where=&order_by=gd_hgnc_id&format=text&limit=&hgnc_dbtag=on&submit=submit" -O hgnc_downloads.txt