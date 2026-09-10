// Materialize pasted screenshots (cmux Cmd+V) into the workspace so they are
// readable by file tools and survive the ephemeral container FS.
//
// opencode receives pasted images as `file` parts carrying
// `data:image/*;base64,...` URLs. This plugin decodes each one into
// .opencode-data/pastes/ (gitignored, inside the mounted /workspace) and
// appends a text part with the durable worktree-relative path.
import { mkdir, writeFile } from "node:fs/promises"
import { join } from "node:path"

const EXTENSIONS = {
  "image/png": "png",
  "image/jpeg": "jpg",
  "image/webp": "webp",
  "image/gif": "gif",
}

export const PasteMaterializer = async ({ worktree, directory }) => {
  const root = worktree ?? directory
  let counter = 0

  return {
    "chat.message": async (_input, output) => {
      for (const part of output.parts) {
        if (part?.type !== "file" || typeof part.url !== "string") continue
        const match = part.url.match(
          /^data:(image\/(?:png|jpeg|webp|gif));base64,([A-Za-z0-9+/=\s]+)$/,
        )
        if (!match) continue

        const mime = match[1]
        const ext = EXTENSIONS[mime]
        const timestamp = new Date().toISOString().replace(/[:.]/g, "-")
        const name = `${timestamp}-${String(counter++).padStart(2, "0")}.${ext}`
        const relative = join(".opencode-data", "pastes", name)
        const absolute = join(root, relative)

        await mkdir(join(root, ".opencode-data", "pastes"), { recursive: true })
        await writeFile(absolute, Buffer.from(match[2], "base64"))

        output.parts.push({
          type: "text",
          text: `Pasted screenshot materialized at ${relative} (worktree-relative). Use this path with file tools.`,
        })
      }
    },
  }
}
