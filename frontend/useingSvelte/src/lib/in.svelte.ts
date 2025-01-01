import ky, { type KyResponse } from "ky"
import { pgInstances, pgState, services, storageStates } from "./store.svelte"
import type { PageState } from "./store.svelte"

export async function updatePageState() {
  const res: KyResponse = await ky.post("http://localhost:8000/api/pagestate/update", { json: { "id": pgState.pageId, "pageState": pgState.pageState[0] } })
  const result = await res.json()
  console.log(result)
  return
}

export async function killBrowser() {
  const res: KyResponse = await ky.post("http://localhost:8000/api/appstate/status", { json: { status: false } })
  const result: { success: string } = await res.json()
  if (result.success) {
    pgInstances.clear()
  }
  return
}

export async function getPageInfoById(id: number) {
  interface Response {
    id: number,
    pageState: PageState
  }
  const res: KyResponse = await ky.get(`http://localhost:8000/api/appstate?id=${id}`)
  const result: Response = await res.json()
  pgState.update(result.id, result.pageState)
  console.log("Ohio")
  return
}

export async function startNewPage() {
  interface Response {
    id: number,
    pageState: PageState
  }
  const serviceIndex: number = (document.getElementById("ServiceDisplay") as HTMLSelectElement).selectedIndex
  const storageState: string = (document.getElementById("StorageDisplay") as HTMLSelectElement).value
  const contextURL: string = (document.getElementById("ContextURL") as HTMLInputElement).value
  const autoLogIn: boolean = (document.getElementById("Autologin") as HTMLInputElement).checked
  const sendData = {
    "serviceIndex": serviceIndex,
    "storageState": storageState,
    "contextURL": contextURL,
    "autoLogIn": autoLogIn
  }
  const res: KyResponse = await ky.post("http://localhost:8000/api/appstate", { json: sendData })
  const result: Response = await res.json()
  console.log("Skibidi")
  pgState.update(result.id, result.pageState)
  pgInstances.addInstance(result.id, result.pageState.service)

  // Skibidi
  return
}

export async function getServices(): Promise<string[]> {
  interface Response {
    service: string[]
  }
  const res: KyResponse = await ky.get("http://localhost:8000/api/appstate/service")
  const result: Response = await res.json()
  services.set(result.service)
  return result.service
}

export async function getStorageStates(): Promise<string[]> {
  interface Response {
    storageState: string[]
  }
  const res: KyResponse = await ky.get("http://localhost:8000/api/appstate/storagestate")
  const result: Response = await res.json()
  storageStates.set(result.storageState)
  return result.storageState
}
