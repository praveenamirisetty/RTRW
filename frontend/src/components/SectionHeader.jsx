export default function SectionHeader({ eyebrow = 'RTRW WORKSPACE', title, description, action }) {
  return (
    <div className="mb-6 flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
      <div>
        <p className="text-xs font-bold uppercase tracking-[0.16em] text-brand-600">{eyebrow}</p>
        <h1 className="mt-2 text-2xl font-bold tracking-tight text-ink sm:text-3xl">{title}</h1>
        {description && <p className="mt-2 text-sm text-slate-500">{description}</p>}
      </div>
      {action}
    </div>
  )
}
