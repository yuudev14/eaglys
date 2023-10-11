"use client"

import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'

import ParserService from '@/services/parser'

export default function Home() {
  const [sql, setSql] = useState<string>("")

  const modifiedSQL = useMutation({
    mutationFn: async (_sql: string) => {
      return await ParserService.hashedSQLColumns(_sql)
    },
  })

  const mappedHasedColumns = useMutation({
    mutationFn: async (_sql: string) => {
      return await ParserService.mappedHashedColumns(_sql)
    },
  })

  const submitHandler = (e: React.FormEvent) => {
    e.preventDefault()
    modifiedSQL.mutate(sql)
    mappedHasedColumns.mutate(sql)
  }



  return (
    <main className="w-full max-w-[1080px] m-auto pt-20">
      <form onSubmit={submitHandler} className='flex flex-col gap-5 w-full max-w-[700px]'>
        <textarea onChange={(e) => setSql(e.target.value)} className='border p-3' />
        <input type="submit" value="Submit" />
      </form>
      {!modifiedSQL.isLoading && modifiedSQL.data && (
        <p><span>Modified SQL:</span> {modifiedSQL.data.data.result}</p>
      )}
      {!mappedHasedColumns.isLoading && mappedHasedColumns.data && (
        <p><span>Modified SQL:</span> <pre>{JSON.stringify(mappedHasedColumns.data.data.result, null, 2)}</pre></p>
      )}

    </main>
  )
}
