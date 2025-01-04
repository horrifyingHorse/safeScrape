import ky, { type KyResponse } from "ky"
import { pgInstances, pgState, services, storageStates, newStateWanted, stateName, logDisplay } from "./store.svelte"
import type { PageState } from "./store.svelte"
import { get } from "svelte/store"

interface APIResponse<T> {
  success: boolean,
  data: T | null,
  error: string | null
}

export async function saveStorageState() {
  const res: KyResponse = await ky.post("http://localhost:8000/api/pagestate/savestoragestate", { json: { "id": pgState.pageId, "pageState": pgState.pageState[0] }, timeout: 20000 })
  const result: APIResponse<null> = await res.json()
  if (!result.success) {
    logDisplay.error("Unable to store state", ["font-bold"])
    logDisplay.error("Server Response: " + result.error)
    return
  }
  newStateWanted.set(false)
  const arr = get(storageStates)
  storageStates.set([...arr, `${get(stateName)}.state`])
  logDisplay.success("Storage state " + get(stateName) + " saved")
  stateName.set("template")
  return
}

export async function updatePageState() {
  const res: KyResponse = await ky.post("http://localhost:8000/api/pagestate/update", { json: { "id": pgState.pageId, "pageState": pgState.pageState[0] } })
  const result: APIResponse<null> = await res.json()
  if (!result.success) {
    logDisplay.error("Failed to update page state with id: " + pgState.pageId, ["font-bold"])
    logDisplay.error("Server Response: " + result.error)
  }
  return
}

export async function killBrowser() {
  logDisplay.log("Killing browser")
  const res: KyResponse = await ky.post("http://localhost:8000/api/appstate/status", { json: { status: false } })
  const result: APIResponse<null> = await res.json()
  if (result.success) {
    pgInstances.clear()
    logDisplay.success("Assassination Completed")
  } else {
    logDisplay.error("Assasination Failed", ["font-bold"])
    logDisplay.error("Server Response: " + result.error)
  }
  return
}

export async function getPageInfoById(id: number) {
  const res: KyResponse = await ky.get(`http://localhost:8000/api/appstate?id=${id}`)
  const result: APIResponse<{ id: number, pageState: PageState }> = await res.json()
  if (result.data === null) {
    logDisplay.error("Error fetching info of page with id: " + id, ["font-bold"])
    logDisplay.error("Server Response: " + result.error)
  } else {
    pgState.update(result.data.id, result.data.pageState)
  }
  return
}

export async function startNewPage() {
  const serviceIndex: number = (document.getElementById("ServiceDisplay") as HTMLSelectElement).selectedIndex
  let storageState: string = ""
  if (get(newStateWanted)) {
    storageState = get(stateName)
  } else {
    storageState = (document.getElementById("StorageDisplay") as HTMLSelectElement).value
  }
  const contextURL: string = (document.getElementById("ContextURL") as HTMLInputElement).value
  const autoLogIn: boolean = (document.getElementById("Autologin") as HTMLInputElement).checked
  const sendData = {
    "serviceIndex": serviceIndex,
    "newStorageState": get(newStateWanted),
    "storageState": storageState,
    "contextURL": contextURL,
    "autoLogIn": autoLogIn
  }
  logDisplay.log("Launching new page: " + get(services)[serviceIndex] + "::" + storageState)
  const res: KyResponse = await ky.post("http://localhost:8000/api/appstate", { json: sendData })
  const result: APIResponse<{ id: number, pageState: PageState }> = await res.json()
  if (result.data === null) {
    logDisplay.error("Failed to launch new page", ["font-bold"])
    logDisplay.error("Server Response: " + result.error)
  } else {
    pgState.update(result.data.id, result.data.pageState)
    pgInstances.addInstance(result.data.id, result.data.pageState.service)
    logDisplay.success("Launched new page")
  }

  // Skibidi
  return
}

export async function getServices(): Promise<string[]> {
  const res: KyResponse = await ky.get("http://localhost:8000/api/appstate/service")
  const result: APIResponse<{ service: string[] }> = await res.json()
  if (result.data === null) {
    logDisplay.error("Error fetching services", ["font-bold"])
    logDisplay.error("Server Response: " + result.error)
    return []
  }
  services.set(result.data.service)
  return result.data.service
}

export async function getStorageStates(): Promise<string[]> {
  const res: KyResponse = await ky.get("http://localhost:8000/api/appstate/storagestate")
  const result: APIResponse<{ storageState: string[] }> = await res.json()
  if (result.data === null) {
    logDisplay.error("Error fetching storage states", ["font-bold"])
    logDisplay.error("Server Response: " + result.error)
    return []
  }
  storageStates.set(result.data.storageState)
  if (get(storageStates).length == 0) {
    newStateWanted.set(true);
  }
  return result.data.storageState
}
