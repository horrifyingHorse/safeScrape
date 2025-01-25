import ky, { type KyResponse } from "ky"
import { indexedDataBaseNames, pgInstances, pgState, services, storageStates, newStateWanted, stateName, logDisplay, upSockConn } from "./store.svelte"
import type { PageState } from "./store.svelte"
import { get } from "svelte/store"

interface APIResponse<T> {
  success: boolean,
  data: T | null,
  error: string | null
}

export async function toggleScrape() {
  const updatedState: boolean = !pgState.pageState[0].scrape
  console.log(updatedState, pgState.pageId)
  const res: KyResponse = await ky.post("http://localhost:8000/api/pagestate/scrape", { json: { "id": pgState.pageId, "status": updatedState } })
  const result: APIResponse<null> = await res.json()
  if (!result.success) {
    logDisplay.error("Failed to update page state with id: " + pgState.pageId, ["font-bold"])
    logDisplay.error("Server Response: " + result.error)
    return
  }
  pgState.pageState[0].scrape = updatedState
  logDisplay.serverlog("Scraping status set to: " + updatedState)
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
    indexedDataBaseNames.forEach(dbName => {
      const dbDel = window.indexedDB.deleteDatabase(dbName)
      dbDel.onsuccess = () =>
        console.log("Successfully Deleted Database: ", dbName)
      dbDel.onerror = () =>
        console.error("Unable to delete Database ", dbName)
      dbDel.onblocked = () =>
        console.warn("Database deletion is blocked. Close all connections to proceed.");
    })
    logDisplay.success("Assassination Completed")
  } else {
    logDisplay.error("Assasination Failed", ["font-bold"])
    logDisplay.error("Server Response: " + result.error)
  }
  return
}

export async function getPageInfoById(id: number) {
  const res: KyResponse = await ky.get(`http://localhost:8000/api/appstate?id=${id}`)
  const result: APIResponse<{ id: number, pageState: PageState, ws_addr: number }> = await res.json()
  if (result.data === null) {
    logDisplay.error("Error fetching info of page with id: " + id, ["font-bold"])
    logDisplay.error("Server Response: " + result.error)
  } else {
    pgState.update(result.data.id, result.data.pageState)
    upSockConn(result.data.ws_addr)
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
  const res: KyResponse = await ky.post("http://localhost:8000/api/appstate", { json: sendData, timeout: 20000 })
  const result: APIResponse<{ id: number, pageState: PageState, ws_addr: number }> = await res.json()
  if (result.data === null) {
    logDisplay.error("Failed to launch new page", ["font-bold"])
    logDisplay.error("Server Response: " + result.error)
  } else {
    pgState.update(result.data.id, result.data.pageState)
    pgInstances.addInstance(result.data.id, result.data.pageState.service)
    logDisplay.success("Launched new page")
    upSockConn(result.data.ws_addr)
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
