export type DataPreviewConfig = {
	previewURL: string;
	data: Record<string, string>[];
	nrow: number;
	ncol: number;
	headers: string[];
	title?: string;
	description?: string;
};
