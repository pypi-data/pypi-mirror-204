import { Fragment, useState } from "react";
import { Dialog, Transition } from "@headlessui/react";
import { XMarkIcon, ArrowsPointingOutIcon } from "@heroicons/react/24/outline";
import clsx from "clsx";
interface Props {
	openText?: string;
	title?: string;
	children: React.ReactNode;
	className?: string;
	network?: boolean;
}

const Body = ({ children }: { children: React.ReactNode }) => {
	return <div className="text-center">{children}</div>;
};

const Modal = ({
	openText,
	children,
	title,
	network,
	className = "sm:max-w-3xl",
}: Props) => {
	const [showModal, setShowModal] = useState(false);
	return (
		<>
			<button
				className="btn btn-outline"
				type="button"
				onClick={() => setShowModal(true)}
			>
				{openText ? openText : <ArrowsPointingOutIcon className='w-6 h-6' />}
			</button>
			{showModal ? (
				<>
					<Transition.Root show={showModal} as={Fragment}>
						<Dialog as="div" className="relative z-10" onClose={setShowModal}>
							<Transition.Child
								as={Fragment}
								enter="ease-out duration-300"
								enterFrom="opacity-0"
								enterTo="opacity-100"
								leave="ease-in duration-200"
								leaveFrom="opacity-100"
								leaveTo="opacity-0"
							>
								<div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
							</Transition.Child>

							<div className="fixed inset-0 z-10 overflow-y-auto">
								<div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
									<Transition.Child
										as={Fragment}
										enter="ease-out duration-300"
										enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
										enterTo="opacity-100 translate-y-0 sm:scale-100"
										leave="ease-in duration-200"
										leaveFrom="opacity-100 translate-y-0 sm:scale-100"
										leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
									>
										<Dialog.Panel
											className={clsx(
												className,
												"relative transform overflow-hidden rounded-lg  px-4 pb-4 text-left shadow-xl transition-all sm:my-4 sm:w-full sm:p-4 bg-base-100",
											)}
										>
											<div className="flex items-center">
												{title && (
													<h3 className='tracking-tight text-gray-50'>
														{title}
													</h3>
												)}
												{network && (
													<h3 className='tracking-tight text-gray-50 text-sm px-4'>
														A website network with circles representing{" "}
														<span className="text-[#a991f7]">analysis </span>
														and <span className="text-[#3b82f6]">data</span>,
														connections are defined by the `relationships`
														frontmatter, focal points are{" "}
														<span className="text-[#eab308]">highlighted</span>.
													</h3>
												)}

												<div className='ml-auto'>
													<button onClick={() => setShowModal(false)}>
														<XMarkIcon className='w-6 h-6' />
													</button>
												</div>
											</div>
											{children}
										</Dialog.Panel>
									</Transition.Child>
								</div>
							</div>
						</Dialog>
					</Transition.Root>
				</>
			) : null}
		</>
	);
};

Modal.Body = Body;

export default Modal;
