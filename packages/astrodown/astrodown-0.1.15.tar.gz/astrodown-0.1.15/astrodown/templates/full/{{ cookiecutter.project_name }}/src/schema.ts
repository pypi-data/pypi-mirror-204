import { z } from "astro:content";

const Relationship = z.union([
	z.string(),
	z.object({
		id: z.string(),
		label: z.string().optional(),
	}),
]);

export const analysisSchema = z.object({
	title: z.string(),
	author: z.union([z.string(), z.array(z.string())]),
	id: z.string().optional(),
	label: z.string().optional(),
	date: z.string().transform((str) => new Date(str)),
	description: z.string().optional(),
	tags: z.array(z.string()).default([]),
	relationships: z.array(Relationship).default([]),
});

export const dataSchema = z.object({
	title: z.string(),
	id: z.string().optional(),
	label: z.string().optional(),
	previewURL: z.string().optional(),
	description: z.string().optional(),
	relationships: z.array(Relationship).default([]),
});
