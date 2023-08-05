import type { DataPreviewConfig } from "src/types";
import Modal from "../shared/Modal";
import Table from "../shared/Table";

export type Props = {
	config: DataPreviewConfig;
};

export default function DataPreview({ config }: Props) {
	const { data, nrow, ncol, headers, title, description, previewURL } = config;
	return (
		<Modal openText="Preview" className="max-w-3xl">
			<Modal.Body>
				<div className="sm:flex sm:items-center">
					<div className="sm:flex-auto">
						{title && (
							<>
								<h2 className="text-2xl leading-6 text-gray-900 font-semibold">
									{title}
								</h2>
								<p>
									{nrow} rows, {ncol} columns
								</p>
								<p>
									<a href={previewURL}>{previewURL}</a>
								</p>
							</>
						)}
						{description && (
							<p className="mt-2 text-sm text-gray-700 text-left">
								{description}
							</p>
						)}
					</div>
				</div>
				{nrow > 100 && (
					<p className="text-sm text-gray-700 text-left mt-2">First 100 rows</p>
				)}
				<Table data={data} headers={headers} />
			</Modal.Body>
		</Modal>
	);
}
